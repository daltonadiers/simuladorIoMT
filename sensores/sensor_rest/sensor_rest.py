from util import Generator, DataBase, postToRest, User
from complex_events import ComplexHealthEventDetector
import time, logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    while True:
        try:
            db = DataBase()
            db.returnActiveUsers()
            if len(users) > 0:
                sg = Generator()
                ce_detector = ComplexHealthEventDetector()
                new_generation = sg.generate(users)
                complex_events = ce_detector.detect_complex_events(new_generation)
                if complex_events:
                    ce_detector.log_complex_events(complex_events)
                pr = postToRest()
                pr.post_users(new_generation)
                logger.info(f"Generated sensor data for {len(users)} users")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error in sensor generation process: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
