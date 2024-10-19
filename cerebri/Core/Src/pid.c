#include "pid.h"


#define DISTANCE_1_TOUR_AXE_TRANSMISSION_MM 500 // Example value, replace with actual one

static uint32_t previous_measure_us = 0;
static uint32_t intervals_array_us[16] = {0};

static float distance_per_interval_us = DISTANCE_1_TOUR_AXE_TRANSMISSION_MM * 1000 / 16.0;
static uint32_t sum_intervals_us = 0;
static uint32_t index = 0;
static uint8_t flag = 0;

float measured_speed_m_s = 0;
float measured_speed_mm_s = 0;
float speed_setpoint_m_s = 0; // Speed setpoint, defined elsewhere

uint32_t watchdog_counter = 0;

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef* htim)
{
    uint32_t current_measure_us;
    uint32_t num_intervals = 0;
    uint32_t i;

    // Get the current timer capture value
    current_measure_us = __HAL_TIM_GET_COMPARE(&htim2, TIM_CHANNEL_1);

    // Check for a valid measurement (ignoring glitches under 300 µs)
    if ((current_measure_us - previous_measure_us) >= 300)
    {
        // If the interval is greater than 100 ms, reset the interval array (new rotation)
        if ((current_measure_us > (previous_measure_us + 100000)) || ((current_measure_us - 100000) > previous_measure_us))
        {
            // Reset interval array and index
            for (index = 0; index < 16; index++)
            {
                intervals_array_us[index] = 0;
            }
            index = 0;
        }
        else // Otherwise, we are in continuous rotation
        {
            flag = 1;
            // Save the new interval
            intervals_array_us[index] = current_measure_us - previous_measure_us;

            // Calculate the sum of intervals up to 100 ms or 16 intervals
            sum_intervals_us = 0;
            num_intervals = 0;
            i = index;
            do {
                if (intervals_array_us[i] == 0)
                    break;

                sum_intervals_us += intervals_array_us[i];
                i = (i - 1) % 16;
                num_intervals++;
            } while ((sum_intervals_us < 100000) && (num_intervals < 16));

            // Increment index with wrap-around at 16
            index = (index + 1) % 16;

            // Calculate the speed in m/s (avoid division by zero)
            if (sum_intervals_us > 0)
            {
                measured_speed_m_s = distance_per_interval_us * num_intervals / sum_intervals_us;
                measured_speed_mm_s = 1000 * measured_speed_m_s; // Convert to mm/s
            }
        }

        // Update the previous measurement
        previous_measure_us = current_measure_us;
    }
}

// Period Elapsed Callback for TIM
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef* htim)
{
    watchdog_counter++;

    float current_speed, setpoint, error;
    static float previous_command = 0, previous_error = 0;
    static uint32_t reverse_flag = 0;
    HAL_GPIO_WritePin(LED2_GPIO_Port, LED2_Pin, 1); // Turn on LED for feedback

    // Capture the measured speed or set to 0 if no valid measurement
    if (flag == 1)
    {
        flag = 0;
        current_speed = measured_speed_m_s;
    }
    else
    {
        current_speed = 0;
        measured_speed_m_s = 0;
        measured_speed_mm_s = 0;
        previous_error = 0;
        previous_command = 0;
    }

    // Setpoint for speed control
    setpoint = speed_setpoint_m_s;

    // If the watchdog timer exceeds 2 seconds, stop the motor
    if (watchdog_counter >= 100)
        setpoint = 0;

    // Calculate the speed error
    error = setpoint - current_speed;

    // PI controller calculation (Proportional-Integral controller)
    float command = previous_command + Kp * ((1 + Te / (2*Ti)) * error + (Te/(2*Ti) - 1) * previous_error);

    // Motor control logic
    if (setpoint == 0)
    {
        send_normalized_cmd(0); // Stop motor
        reverse_flag = 0;
    }
    else if (setpoint < 0 && reverse_flag == 0)
    {
    	send_normalized_cmd(-10.0); // Initial reverse command
        reverse_flag++;
    }
    else if (setpoint < 0 && reverse_flag == 1)
    {
        reverse_flag++;
        send_normalized_cmd(0); // Stop motor after initial reverse
    }
    else if (setpoint < 0 && reverse_flag == 2)
    {
        command = Kp * setpoint; // Apply reverse speed
        send_normalized_cmd(command);
    }
    else
    {
    	send_normalized_cmd(command); // Apply forward speed
        reverse_flag = 0;
    }

    // Update previous values for the next cycle
    previous_command = command;
    previous_error = error;

    HAL_GPIO_WritePin(LED2_GPIO_Port, LED2_Pin, 0); // Turn off LED
}