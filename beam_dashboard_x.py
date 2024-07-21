import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import argparse


@st.cache_data
def parse_args():
    parser = argparse.ArgumentParser(
                    prog='dashboard',
                    description='PLAID Dashboard to review results of FLASH optimizations',
                    epilog='v0.1.0')
    parser.add_argument('--plan-id', required=True)
    parser.add_argument('--course-id', required=True)
    parser.add_argument('--patient-id', required=True)
    parser.add_argument('--accept-Varian-LUSLA', action='store_true')

    return parser.parse_args()

args = parse_args()

plan_id = args.plan_id
course_id = args.course_id
patient_id = args.patient_id


@st.cache_data # this keeps streamlit from re-loading ESAPI (avoids atomic access violation)
def extract_data(patient_id, course_id, plan_id):
    print("Launching PyESAPI...")
    import pyesapi
    
    print("Creating ESAPI app instance...")
    _app = pyesapi.CustomScriptExecutable.CreateApplication('dashboard_pro')
    
    try:
        patient = _app.OpenPatientById(patient_id)
        plan = patient.CoursesLot(course_id).PlanSetupsLot(plan_id)

        beams_df = None
        print("Extracting beam data...")
        for beam in plan.Beams:
            beamMetersetValue = beam.Meterset.Value
            totMetersetWeight = [cpp for cpp in beam.ControlPoints][-1].MetersetWeight
            eParams = beam.GetEditableParameters()
        #    for idx, controlPoint in enumerate(eParams.ControlPoints):
            beams_df = pd.concat([beams_df, pd.DataFrame({
                'Field ID': beam.Id,
                'Technique': beam.Technique.ToString(),
                'MU': np.diff(np.array([0]+[cp.MetersetWeight for cp in eParams.ControlPoints])*beamMetersetValue/totMetersetWeight),
                'Gantry Angle' : [cp.GantryAngle for cp in eParams.ControlPoints]
                # add other data elments of interest here
            })])

        # load structure data
        structures_df = None
        for structure in plan.StructureSet.Structures:
            dvh = plan.GetDVHCumulativeData(
                structure,
                pyesapi.DoseValuePresentation.Relative,
                pyesapi.VolumePresentation.Relative,
                .1
            )
            if dvh is not None:
                structures_df = pd.concat([structures_df, pd.DataFrame({
                    'Structure ID': structure.Id,
                    'Color': "#" + structure.Color.ToString()[3:],  # format is '#AARRGGBB'
                    'Dose %': [p.DoseValue.Dose for p in dvh.CurveData],
                    'Volume %': [p.Volume for p in dvh.CurveData],
                })])
        
        # load target contour outline data in beams-eye-view
        bev_df = None
        plan_target = plan.StructureSet.StructuresLot(plan.TargetVolumeID)
        for beam in plan.Beams:
            for idx, contour in enumerate(beam.GetStructureOutlines(plan_target,True)):
                bev_df = pd.concat([bev_df, pd.DataFrame({
                    'Beam ID' : beam.Id,
                    'Structure ID': plan_target.Id,
                    'Color': "#" + plan_target.Color.ToString()[3:],
                    'Points X' : [p.X for p in contour],
                    'Points Y' : [p.Y for p in contour],
                    'Contour Idx' : idx,
                })])

        # TODO: check if plan is Static Gantry or VMAT

    except Exception as e:
        raise e
    finally:
        print('Cleaning up...')
        _app.ClosePatient()
        _app.Dispose()
        print('Done!')

    return beams_df, structures_df, bev_df


st.title("BeamDashboardX")
expander = st.expander("Use of this software is bound by the terms of the Varian LULSA (click to show/hide)", expanded=not args.accept_Varian_LUSLA)
expander.write("""
VARIAN LIMITED USE SOFTWARE LICENSE AGREEMENT

This Limited Use Software License Agreement (the "Agreement") is a legal agreement between you , the
user (“You”), and Varian Medical Systems, Inc. ("Varian"). By downloading or otherwise accessing the
software material, which includes source code (the "Source Code") and related software tools (collectively,
the "Software"), You are agreeing to be bound by the terms of this Agreement. If You are entering into this
Agreement on behalf of an institution or company, You represent and warrant that You are authorized to do
so. If You do not agree to the terms of this Agreement, You may not use the Software and must immediately
destroy any Software You may have downloaded or copied.

SOFTWARE LICENSE

1. Grant of License. Varian grants to You a non-transferable, non-sublicensable license to use
the Software solely as provided in Section 2 (Permitted Uses) below. Access to the Software will be
facilitated through a source code repository provided by Varian.

2. Permitted Uses. You may download, compile and use the Software, You may (but are not required to do
so) suggest to Varian improvements or otherwise provide feedback to Varian with respect to the
Software. You may modify the Software solely in support of such use, and You may upload such
modified Software to Varian’s source code repository. Any derivation of the Software (including compiled
binaries) must display prominently the terms and conditions of this Agreement in the interactive user
interface, such that use of the Software cannot continue until the user has acknowledged having read
this Agreement via click-through.

3. Publications. Solely in connection with your use of the Software as permitted under this Agreement, You
may make reference to this Software in connection with such use in academic research publications
after notifying an authorized representative of Varian in writing in each instance. Notwithstanding the
foregoing, You may not make reference to the Software in any way that may indicate or imply any
approval or endorsement by Varian of the results of any use of the Software by You.

4. Prohibited Uses. Under no circumstances are You permitted, allowed or authorized to distribute the
Software or any modifications to the Software for any purpose, including, but not limited to, renting,
selling, or leasing the Software or any modifications to the Software, for free or otherwise. You may not
disclose the Software to any third party without the prior express written consent of an authorized
representative of Varian. You may not reproduce, copy or disclose to others, in whole or in any part, the
Software or modifications to the Software, except within Your own institution or company, as applicable,
to facilitate Your permitted use of the Software. You agree that the Software will not be shipped,
transferred or exported into any country in violation of the U.S. Export Administration Act (or any other
law governing such matters) and that You will not utilize, in any other manner, the Software in
violation of any applicable law.

5. Intellectual Property Rights. All intellectual property rights in the Software and any modifications to
the Software are owned solely and exclusively by Varian, and You shall have no ownership or other
proprietary interest in the Software or any modifications. You hereby transfer and assign to Varian all
right, title and interest in any such modifications to the Software that you may have made or contributed.
You hereby waive any and all moral rights that you may have with respect to such modifications, and
hereby waive any rights of attribution relating to any modifications of the Software. You acknowledge
that Varian will have the sole right to commercialize and otherwise use, whether directly or through third
parties, any modifications to the Software that you provide to Varian’s repository. Varian may make any
use it determines to be appropriate with respect to any feedback, suggestions or other communications
that You provide with respect to the Software or any modifications.

6. No Support Obligations. Varian is under no obligation to provide any support or technical assistance in
connection with the Software or any modifications. Any such support or technical assistance is entirely
discretionary on the part of Varian, and may be discontinued at any time without liability.

7. NO WARRANTIES. THE SOFTWARE AND ANY SUPPORT PROVIDED BY VARIAN ARE PROVIDED
“AS IS” AND “WITH ALL FAULTS.” VARIAN DISCLAIMS ALL WARRANTIES, BOTH EXPRESS AND
IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT WITH RESPECT TO THE
SOFTWARE AND ANY SUPPORT. VARIAN DOES NOT WARRANT THAT THE OPERATION OF THE
SOFTWARE WILL BE UNINTERRUPTED, ERROR FREE OR MEET YOUR SPECIFIC
REQUIREMENTS OR INTENDED USE. THE AGENTS AND EMPLOYEES OF VARIAN ARE NOT
AUTHORIZED TO MAKE MODIFICATIONS TO THIS PROVISION, OR PROVIDE ADDITIONAL
WARRANTIES ON BEHALF OF VARIAN.

8. No Regulatory Clearance. The Software is not cleared or approved for use by any regulatory body in any
jurisdiction.

9. Termination. You may terminate this Agreement, and the right to use the Software, at any time upon
written notice to Varian. Varian may terminate this Agreement, and the right to use the Software, at any
time upon notice to You in the event that Varian determines that you are not using the Software in
accordance with this Agreement or have otherwise breached any provision of this Agreement. The
Software, together with any modifications to it or any permitted archive copy thereof, shall be destroyed
when no longer used in accordance with this Agreement, or when the right to use the Software is
terminated.

10. Limitation of Liability. IN NO EVENT SHALL VARIAN BE LIABLE FOR LOSS OF DATA, LOSS OF
PROFITS, LOST SAVINGS, SPECIAL, INCIDENTAL, CONSEQUENTIAL, INDIRECT OR
OTHER SIMILAR DAMAGES ARISING FROM BREACH OF WARRANTY, BREACH OF
CONTRACT, NEGLIGENCE, OR OTHER LEGAL THEORY EVEN IF VARIAN OR ITS AGENT HAS
BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES, OR FOR ANY CLAIM BY ANY OTHER
PARTY.

11. Indemnification. You will defend, indemnify and hold harmless Varian, its affiliates and their respective
officers, directors, employees, sublicensees, contractors, users and agents from any and all claims,
losses, liabilities, damages, expenses and costs (including attorneys’ fees and court costs) arising out of
any third-party claims related to or arising from your use of the Software or any modifications to the
Software.

12. Assignment. You may not assign any of Your rights or obligations under this Agreement without the
written consent of Varian.

13. Governing Law. This Agreement will be governed and construed under the laws of the State of California
and the United States of America without regard to conflicts of law provisions. The parties agree to the
exclusive jurisdiction of the state and federal courts located in Santa Clara County, California with
respect to any disputes under or relating to this Agreement.

14. Entire Agreement. This Agreement is the entire agreement of the parties as to the subject matter and
supersedes all prior written and oral agreements and understandings relating to same. The Agreement
may only be modified or amended in a writing signed by the parties that makes specific reference to the
Agreement and the provision the parties intend to modify or amend.

Note: To auto-collapse this license agreement display, see the ESAPI .cs file.
""")

plan_title = f'Plan ID: {plan_id}\nPatient ID: {patient_id} | Course ID: {course_id}'
st.title(plan_title)

beams_df, structures_df, bev_df = extract_data(patient_id, course_id, plan_id)
st.header('Raw Field Data')
st.download_button(
   "Download (.csv)",
   beams_df.to_csv(index=False).encode('utf-8'),
   "raw_data.csv",
   "text/csv",
   key='download-csv'
)
st.dataframe(beams_df, use_container_width=True) # creates a table


##
st.header('TODO: Beam stats')
##

#################
#  Static/IMRT  #
#################
# if beams_df.iloc[0]['Technique'] in ['Static', 'MLC', 'MultipleStaticSegmentIMRT', 'SlidingWindowIMRT']:
#     ##
#     st.header("Beam's eye view")
#     ##

#     for fld_name, field_df in beams_df.groupby('Field ID'):
#         # st.subheader(fld_name)
#         fig_scatt = go.Figure()
#         for _, bev_field in bev_df[bev_df['Beam ID'] == fld_name].groupby('Contour Idx'):
#             # TODO: loop through structures:
#             structure_id = bev_field['Structure ID'][0]
#             fig_scatt.add_trace(go.Scatter(
#             x=bev_field['Points X'], y=bev_field['Points Y'],
#                 mode='lines', line_color=bev_field['Color'][0], name=structure_id
#             ))

#             # fig_scatt.update_traces(line_color=dfc_field['Color'][0], selector=dict(name='PTV'))

#         #st.plotly_chart(fig_scatt, use_container_width=True)
#         fig_scatt.update_yaxes(
#             scaleanchor="x",
#             scaleratio=1,
#         )
#         
#         st.plotly_chart(fig_scatt, use_container_width=True)

################
#   Arc/VMAT   #
################
if beams_df.iloc[0]['Technique'] in ['VMAT', 'Arc', 'MLCArc']:
    st.subheader('Beam MU Histograms')
    # TODO: implement MU as a function of gantry (VMAT)


###################
st.header('DVH')  #
###################
#TODO: make cursor white!
# get handle on this: <rect class="nsewdrag drag" data-subplot="xy" x="61" y="100" width="499" height="270" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect>
# ... and set cursor style

dvh_fig = go.Figure()
for structure_id, dvh_data in structures_df.groupby('Structure ID'):
    dvh_fig.add_trace(go.Scatter(
        x=dvh_data['Dose %'], y=dvh_data['Volume %'], mode='lines', line_color=dvh_data['Color'][0], name=structure_id
    ))
dvh_fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    legend=dict(
        font=dict(color='white')
    ),
    title = dict(
    text=plan_title.replace('\n',' | '),
        font=dict(color='white')
    ),
    yaxis = dict(
        title='Volume [%]',
        gridcolor='grey'
    ),
    xaxis = dict(
        title = 'Dose [%]',
        showgrid=True,
        gridcolor='grey',
    )
)

st.plotly_chart(dvh_fig, use_container_width=True)
