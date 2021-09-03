from datetime import datetime, timedelta
from send_email import create_message, error_message, send_email_with_contracts, send_empty_email
from get_contracts_from_clearspending import ClearSpending
import time
import traceback
import logging
from email_reciepients import recipients

def main():
    try:
        time1 = time.time()
        start_date, end_date = get_dates()
        for recipient in recipients:
            try:
                region = recipient['region']
                email_list = [el['email'] for el in recipient['recipients']]
                contracts_44 = ClearSpending(daterange=f'{start_date}-{end_date}', customerregion=region[0], fz=44).get_contracts(limit=5)
                contracts_223 = ClearSpending(daterange=f'{start_date}-{end_date}', customerregion=region[0], fz=223).get_contracts(limit=5)
                if not len(contracts_44) and not len(contracts_223):
                    send_empty_email(start_date, email_list, region[1])
                else:
                    message = create_message([*contracts_44, *contracts_223], region[1])
                send_email_with_contracts(message, email_list)
                time.sleep(2)
            except Exception:
                logger.exception(f'ERROR while parsing contracts for recipient {(region[0], region[1])}')

            
        time2 = time.time()
        difference = time2 - time1
        logger.info(f'Succesfully run the project. Exection took {difference} sec')

    except Exception:
        logger.exception('ERROR')
        error_message(traceback.format_exc())
   
def get_dates():
    fist_date_obj = datetime.now() - timedelta(days=8)
    first_date = fist_date_obj.strftime('%d.%m.%Y')
    second_date_obj = datetime.today() - timedelta(days=3)
    second_date = second_date_obj.strftime('%d.%m.%Y')
    return first_date, second_date  

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s')
    file_handler = logging.FileHandler('logs/main.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    main()