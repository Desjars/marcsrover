import zenoh, time, cv2, numpy as np

def listener(sample):
    print(f"Received")
    # Decode jpeg image
    img = np.frombuffer(bytes(sample.value.payload), dtype=np.uint8)
    
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    
    cv2.imshow('image', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return
    

        
if __name__ == "__main__":
    # load config
    config = zenoh.Config.from_file("config.json")
    session = zenoh.open(config)
    sub = session.declare_subscriber('marcsrover/image', listener)
    while True:
        continue