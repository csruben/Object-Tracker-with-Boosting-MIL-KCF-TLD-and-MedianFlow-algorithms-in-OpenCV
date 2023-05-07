import cv2

def ask_for_tracker():
    # Display a menu to let the user choose a tracking algorithm
    print("Welcome! What Tracker API would you like to use?")
    print('Enter 0 for BOOSTING: ')
    print('Enter 1 for MIL: ')
    print('Enter 2 for KCF: ')
    print('Enter 3 for TLD: ')
    print('Enter 4 for MEDIANFLOW: ')
    ch = input("Please select your tracker: ")

    # Use the user's input to select a tracker and return it
    if ch == "0":
        tracker = cv2.TrackerBoosting_create()
    elif ch == "1":
        tracker = cv2.TrackerMIL_create()
    elif ch == "2":
        tracker = cv2.TrackerKCF_create()
    elif ch == "3":
        tracker = cv2.TrackerTLD_create()
    elif ch == "4":
        tracker = cv2.TrackerMedianFlow_create()
    else:
        # Handle invalid input by selecting the first tracker (BOOSTING)
        print("Invalid input! Using BOOSTING tracker by default.")
        tracker = cv2.TrackerBoosting_create()

    return tracker


def main():
    # Ask the user to select a tracker
    tracker = ask_for_tracker()
    # Get the name of the selected tracker for display purposes
    tracker_name = str(tracker).split()[0][1:]

    # Open a video capture device (camera)
    cap = cv2.VideoCapture(0)

    # Read the first frame from the camera and ask the user to select a region of interest (ROI)
    ret, frame = cap.read()
    roi = cv2.selectROI(frame, False)

    # Initialize the tracker with the first frame and ROI
    ret = tracker.init(frame, roi)

    # Loop through all subsequent frames from the camera
    while True:
        # Read the next frame from the camera
        ret, frame = cap.read()

        # Use the tracker to update the position of the tracked object in the current frame
        success, roi = tracker.update(frame)

        # Convert the ROI to integer coordinates for drawing a rectangle around the tracked object
        (x, y, w, h) = tuple(map(int, roi))

        # If tracking is successful, draw a green rectangle around the tracked object; otherwise, display a failure message
        if success:
            p1 = (x, y)
            p2 = (x + w, y + h)
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Failure to Detect Tracking!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        # Display the current frame with the tracked object highlighted
        cv2.imshow(tracker_name, frame)

        # Wait for the user to press the ESC key to exit the program
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
