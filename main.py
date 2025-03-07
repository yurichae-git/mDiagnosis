from pages.test_01_mobileDiagnosis import Reservation
from pages.test_02_vehicle_info import VehicleInfo
from pages.test_03_vehicle_option import VehicleOption
from pages.test_04_diagnosis import Diagnosis
from playwright.sync_api import sync_playwright






def main():
    # Use a breakpoint in the code line below to debug your script.
    with sync_playwright() as playwright:


        Reservation(playwright)
        #VehicleInfo(playwright)
        #VehicleOption(playwright)
        #Diagnosis(playwright)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
