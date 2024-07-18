using System;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using System.Collections.Generic;
using VMS.TPS.Common.Model.API;
using VMS.TPS.Common.Model.Types;
using System.Reflection;
using System.IO;
using System.Diagnostics;
using System.Runtime.CompilerServices;

// [assembly: ESAPIScript(IsWriteable = true)]

namespace VMS.TPS
{
    public class Script
    {
        public void Execute(ScriptContext context)  //, System.Windows.Window window, ScriptEnvironment environment)
        {
            (new DashboardX()).Execute(context);
        }
    }

    public class DashboardX
    {
        // for use in development environment with virtual environment
        const string DEV_PYTHON_ENV = "venv";
        const string DEV_PYTHON_EXE = "python.exe";

        public void Execute(ScriptContext context)
        {
            this.LaunchDashboard(context);
        }
        public void LaunchDashboard(ScriptContext context, [CallerFilePath] string pathHere = "")
        {
            var workingDirectory = Path.GetDirectoryName(pathHere);
            bool runningInProduction = true;
            
            if(File.Exists(Path.Combine(workingDirectory, "streamlit_runner.py")))
            {
                // streamlit_runner.py should not be in the production environment
                runningInProduction = false;
            }

            var scriptPath = Path.Combine(workingDirectory, "beam_dashboard_x.py");
            string exePath;

            if(runningInProduction)
            {
                exePath = "\"" + Path.Combine(workingDirectory, "streamlit_runner", "streamlit_runner.exe") + "\"";
            }
            else  // development mode
            {
                exePath = "\"" + Path.Combine(workingDirectory, DEV_PYTHON_ENV, "Scripts", DEV_PYTHON_EXE) + "\"";
                scriptPath = "\"" + Path.Combine(workingDirectory, "streamlit_runner.py") + "\" \"" + scriptPath + "\"";
            }

            
            var startInfo = new ProcessStartInfo(exePath);
            startInfo.UseShellExecute = false;                        
            startInfo.Arguments = scriptPath +
                ArgBuilder("plan-id", context.PlanSetup.Id) +
                ArgBuilder("course-id", context.PlanSetup.Course.Id) +
                ArgBuilder("patient-id", context.Patient.Id);
            
            // uncomment below if you have read and agree to the Varian-LUSLA
            // startInfo.Arguments += " --accept-Varian-LUSLA";

            // uncomment below to help with debugging
            MessageBox.Show(exePath + " " + startInfo.Arguments,"Arguments (press ctrl+c to copy to clipboard)");
            var py = Process.Start(startInfo);
        }
        
        public static String ArgBuilder(String key, String value)
        {
            var cleanValue = value == null ? "" : value;
            return " --" + key + " \"" + cleanValue + "\"";
        }

    }
}
