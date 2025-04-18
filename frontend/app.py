import streamlit as st
import requests
import json

st.set_page_config(page_title="Customer Ticket Resolver", layout="centered")

st.title("Customer Ticket Resolver")

if 'ticket' not in st.session_state:
    st.session_state.ticket = None
if 'similar_tickets' not in st.session_state:
    st.session_state.similar_tickets = []

with st.form(key='ticket_form'):
    issue_description = st.text_input("Describe your issue", "")
    submit_button = st.form_submit_button(label="Submit Ticket")

    if submit_button and issue_description:
        try:
            request_data = {"issue_description": issue_description}
            st.write("Sending request with data:", request_data)

            response = requests.post(
                "http://localhost:8000/submit_ticket",
                json=request_data,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            response.raise_for_status()

            st.write("Raw response status code:", response.status_code)
            st.write("Raw response text:", response.text)

            ticket_data = response.json()
            st.write("Parsed response data:", ticket_data)

            expected_keys = ['ticket_id', 'issue_description', 'category', 'draft_response']
            if all(key in ticket_data for key in expected_keys):
                st.session_state.ticket = ticket_data
                st.success("Ticket submitted successfully!")
                
                # Fetch similar tickets
                similar_response = requests.get(
                    f"http://localhost:8000/similar_tickets/{ticket_data['ticket_id']}",
                    headers={"Accept": "application/json"}
                )
                similar_response.raise_for_status()
                st.session_state.similar_tickets = similar_response.json()
                st.write("Similar tickets fetched:", st.session_state.similar_tickets)
            else:
                st.error(f"Invalid response from server: missing expected fields. Response: {str(ticket_data)}. Expected keys: {expected_keys}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error submitting ticket: {str(e)} - Response: {e.response.text if e.response else 'No response'}")
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON response: {str(e)} - Raw response: {response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

if st.session_state.ticket and all(key in st.session_state.ticket for key in ['ticket_id', 'issue_description', 'category', 'draft_response']):
    st.subheader("Ticket Details")
    st.write(f"**Ticket ID:** {st.session_state.ticket['ticket_id']}")
    st.write(f"**Issue Description:** {st.session_state.ticket['issue_description']}")
    st.write(f"**Category:** {st.session_state.ticket['category']}")
    st.write(f"**Status:** Pending")
    st.write(f"**Draft Response:** {st.session_state.ticket['draft_response']}")
    
    # Display similar tickets with all attributes
    if st.session_state.similar_tickets:
        st.subheader("Similar Tickets")
        for i, similar in enumerate(st.session_state.similar_tickets, 1):
            st.write(f"**{i}. Ticket ID:** {similar['ticket_id']}")
            st.write(f"**Issue:** {similar['issue_description']}")
            st.write(f"**Category:** {similar['category']}")
            st.write(f"**Resolution:** {similar['resolution']}")
            st.write(f"**Similarity Score:** {similar['similarity_score']:.2f}%")
            st.write("---")
    else:
        st.write("No similar tickets found.")
    
    if st.button("Clear"):
        st.session_state.ticket = None
        st.session_state.similar_tickets = []
else:
    if st.session_state.ticket is not None and not all(key in st.session_state.ticket for key in ['ticket_id', 'issue_description', 'category', 'draft_response']):
        st.error("Ticket data is incomplete. Response: " + str(st.session_state.ticket))