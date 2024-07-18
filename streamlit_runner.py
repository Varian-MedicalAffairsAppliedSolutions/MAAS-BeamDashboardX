import streamlit.web.cli as stcli
import sys
from datetime import datetime
from expiration import EXP_DATE

if __name__ == "__main__":
    print("BeamDashboardX is valid until " + EXP_DATE.isoformat())
    print("Check here for the latest releases:")
    print("https://github.com/Varian-MedicalAffairsAppliedSolutions/MAAS-BeamDashboardX/releases")
    print("**Not Validated for Clinical Use**")
    # comment previous line if software has been validated for use in your clinic
    # see license.txt for full disclaimer and details

    if(datetime.today() > EXP_DATE):
        print("[ERROR] This software has expired.")
        sys.exit(99)

    if len(sys.argv) == 1:
        print('ERROR: please provide path to streamlit script')
        sys.exit(1)

    script_path = sys.argv[1]  # first argument should be the path to the streamlit script
    script_args = sys.argv[2:]  # additional arguments are passed along to the streamlit script
    
    # patch sys arguments to be picked up by streamlit main
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
        "--"
    ] + script_args
    sys.exit(stcli.main())
