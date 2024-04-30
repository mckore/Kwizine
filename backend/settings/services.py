import logging

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
                                      # This will load the app logger

class EchoService:
  def echo(self, msg):
    logger.info("echoing something from the app logger")
    print(msg)