import requests
import json
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import os

BASE_API_URL = os.environ.get('BASE_API_URL')
LANGFLOW_ID = os.environ.get('LANGFLOW_ID')
FLOW_ID = os.environ.get('FLOW_ID')
APPLICATION_TOKEN = os.environ.get('APPLICATION_TOKEN')
ENDPOINT=os.environ.get('ENDPOINT')
def run_flow(message: str,) ->dict:
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Social Media engagement analysis")
    message=st.text_area("Message",placeholder="Type something here")
    if st.button("Get Results"):
        try:
            with st.spinner("Loading..."):
                data=run_flow(message)
                print("Before extracting",data)
                data=data['outputs'][0]['outputs'][0]['results']['message']['text']
                print("After extraction data",data)
                data=data.strip('```').strip()
                data=data.strip()
                print("After stripping data",data)
                root=ET.fromstring(data)
                mainData=root.find(".//analysis").text
                print("this is the main data ",mainData)
                st.markdown(mainData,unsafe_allow_html=True)
                
                # parsing the data
                
                likes_distribution=root.find(".//likes_distribution").text
                shares_distribution=root.find(".//shares_distribution").text
                chart_distribution=root.find(".//chart").text
    
                likes_distribution=likes_distribution.split(",")
                shares_distribution=shares_distribution.split(",")
                chart_distribution=chart_distribution.split(",")
                chart_distribution = [int(x) for x in chart_distribution]
                
                
                
                # bargraph for distribution of likes with months
                chart_label=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
                st.title("Likes across various months of the Year")
                plt.figure(figsize=(10,6))
                plt.bar(chart_label,chart_distribution,color="blue")
                plt.title("Likes across various months")
                plt.xlabel("Months")
                plt.ylabel("No. of likes")
                st.pyplot(plt)
                # graph plotting for likes distribution
                ls_label=["Reel","Carousal","Static_Image"]
                fig, ax = plt.subplots(figsize=(4, 4))  # Create a figure and axis
                ax.pie(likes_distribution, labels=ls_label, startangle=90)
                ax.set_title('Distribution of Likes')
                st.pyplot(fig)
                # graph plotting for shares distribution
                fig, ax = plt.subplots(figsize=(4, 4))  # Create a figure and axis
                ax.pie(shares_distribution, labels=ls_label, startangle=90)
                ax.set_title('Distribution of Shares')
                st.pyplot(fig)
        except Exception as e:
            st.error(str(e))



if __name__=="__main__":
   main()
