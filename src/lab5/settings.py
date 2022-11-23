from pydantic import BaseSettings, Field, AnyUrl


class _Settings(BaseSettings):
    """
    This class will read settings from environment variables or '.env' file.
    """

    AMQP_URL: AnyUrl = Field(description='The URL to the rabbitmq in the format of amqp://user:password@host:port.')
    DATABASE_URL: AnyUrl = Field(
        description='The URL to the postgres in the format of postgres://user:password@host:port.'
    )
    AMQP_QUEUE: str = Field(default='lab5', description='Name of the queue, that will be used.')

    class Config:
        """
        This is config for the settings class.
        """

        # Disable case-sensitive variables names. This means you can use 'TV_LAB5_AMQP_URL' or 'tv_lab5_amqp_url'.
        case_sensitive = False

        # Path to '.env' file. This file should be located at the same level as 'src' directory.
        env_file = '../.env'
        # This means, that actual names will be like 'TV_LAB5_AMQP_URL' to avoid any possible coalition.
        env_prefix = 'TV_LAB5_'


# Let 'settings' will be a singleton, that is accessible in any point of project.
settings = _Settings()
