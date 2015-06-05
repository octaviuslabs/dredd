import os


def main():
    print "Setting Up Environment"
    os.environ["TEST"] = str(raw_input('MEM_STORE_HOST: '))
    # os.environ["MEM_STORE_HOST"] = str(raw_input('MEM_STORE_HOST: '))
    # os.environ["MEM_STORE_PORT"] = str(raw_input('MEM_STORE_PORT: '))
    # os.environ["MEM_STORE_DB"] = str(raw_input('MEM_STORE_DB: '))
    # os.environ["MEM_STORE_TYPE"] = "redis"
    # os.environ["POLL_INTERVAL"] = str(raw_input('POLL_INTERVAL: '))
    # os.environ["AWS_ACCESS_KEY_ID"] = str(raw_input('AWS_ACCESS_KEY_ID: '))
    # os.environ["AWS_SECRET_ACCESS_KEY"] = str(raw_input('AWS_SECRET_ACCESS_KEY: '))
    # os.environ["Q_TOWATCH"] = str(raw_input('Q_TOWATCH: '))
    # os.environ["AWS_Q_REGION"] = str(raw_input('AWS_Q_REGION: '))


if __name__ == "__main__":
    main()
