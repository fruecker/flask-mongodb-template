import threading

class TestWorker():

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print("Starting Test Worker...")
        
        try:
            # Do something
            pass
        except Exception as e:
            print("Error:", e)
            
        print("Finished Test Worker.")