import streamlit as st
import pandas as pd
import json

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

option = st.selectbox(
   "How would you like to be contacted?",
   ("MySQL", "BigQuery"), index=None, placeholder="Choose One"
)

if option == 'MySQL' or option == 'BigQuery':
    st.write("You choose ", option)
else:
    st.write("You didn't choose data source")

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df   = conn.query('SELECT * from write_smart_recom_feedback LIMIT 100;', ttl=600)

# import pandas as pd
# cols  = ['jenis_barang', 'jumlah_barang']
# df_pd = pd.DataFrame(df, columns=cols)
# Print results.
# for row in df.itertuples():
#     st.write(f"{row.jenis_barang} has a :{row.jumlah_barang}:")
st.write(df)
# print(type(df))

import streamlit.components.v1 as components

# components.iframe("https://labs.leniolabs.com/data-dashboard/", width=1000, height=500)
components.iframe("http://localhost:3000", width=1000, height=500)
# data = st.file_uploader("Upload a CSV")

# query = st.text_area("Insert your query")

# if st.button("Submit Query", type="primary"):
#     # Create an agent from the CSV file.
#     agent = create_agent(data)

#     # Query the agent.
#     response = query_agent(agent=agent, query=query)

#     # Decode the response.
#     decoded_response = decode_response(response)

#     # Write the response to the Streamlit app.
#     write_response(decoded_response)
