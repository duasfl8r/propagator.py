LOGGING = {
    "version": 1,
    "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "long",
                "filename": "art.log"
                },

            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "short",
                }
            },
    "loggers": {
        "art": {
            "handlers":["console", "file"],
            "level": "DEBUG",
            }
        },

    "formatters": {
        "short": {
            "format": "%(message)s"
        },

        "long": {
            "format": "%(filename)s:%(lineno)s\t%(message)s"
        }
    }
}
