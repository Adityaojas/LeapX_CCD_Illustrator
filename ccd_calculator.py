import streamlit as st
import plotly.graph_objects as go

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Function to check credentials (only by password now)
def authenticate(password):
    return password == st.secrets['PASSWORD']

# Login Screen
if not st.session_state['authenticated']:
    st.title("Login to Access the Application")

    # Removed username input
    password = st.text_input("Password", type="password")

    if st.button("Login") or st.session_state.get('press_enter', False):
        if authenticate(password):
            st.session_state['authenticated'] = True
            st.experimental_rerun()
        else:
            st.error("Incorrect password.")
            st.session_state['press_enter'] = False  # Reset it for subsequent attempts
    
    # Adjusted to trigger login without needing a dummy input
    if st.session_state.get('press_enter', False):
        setattr(st.session_state, 'press_enter', False)  # Reset immediately to avoid looping

else:
    # Constants
    VALUATION_CAP_USD = 2500000
    FLOOR_VALUATION_USD = 1500000
    TOTAL_SHARES_ISSUED = 100000  # Rs
    USD_TO_INR_RATE = 83  # Assume 1 USD = 83 INR for conversion
    MILLION = 1000000

    def calculate_price_per_share_based_on_valuation(valuation_usd, shares_issued):
        return valuation_usd * USD_TO_INR_RATE / shares_issued  # Rs

    def calculate_pre_money_valuation_inr(valuation_usd_m):
        return valuation_usd_m * MILLION * USD_TO_INR_RATE / 10**7  # Crore

    def calculate_pre_money_price_per_share(valuation_inr_cr):
        return valuation_inr_cr * 100

    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 2.5em;
            }
        </style>
        
        <div class="title">LeapX Investment Growth Illustration</div>
        """, unsafe_allow_html=True)
    
    def calculate_price_per_share_for_user(predicted_valuation_usd_m):
        valuation_cap_usd = VALUATION_CAP_USD
        seventy_five_percent_of_predicted = predicted_valuation_usd_m * MILLION * 0.75
        lesser_valuation = min(valuation_cap_usd, seventy_five_percent_of_predicted)
        return calculate_price_per_share_based_on_valuation(lesser_valuation, TOTAL_SHARES_ISSUED)

    col_0_1, col_0_2, col_0_3 = st.columns([2,0.1,2])
    with col_0_1:
        investment_amount_str = st.text_input("The amount you're willing to invest (in Rs)", value="500000")
        try:
            investment_amount = float(investment_amount_str)
        except ValueError:
            st.error("Please enter a valid number for the investment amount.")
            investment_amount = 0  # or set a default fallback value

    with col_0_2:
        # Using markdown with custom HTML for the info icon
        st.markdown("""
            <style>
                .tooltip {
                    position: relative;
                    display: inline-block;
                }
                
                .tooltip .tooltiptext {
                    visibility: hidden;
                    width: 580px;
                    background-color: grey;
                    color: #fff;
                    text-align: center;
                    border-radius: 20px;
                    padding: 20px 5;
                    
                    /* Position the tooltip text */
                    position: absolute;
                    z-index: 1;
                    bottom: 100%;
                    left: 50%;
                    margin-left: -60px;
                }
                
                .tooltip:hover .tooltiptext {
                    visibility: visible;
                }
            </style>
            <div class="tooltip">ℹ️
                <span class="tooltiptext">Valuation Cap for FnF round is set at $2.5M and the floor is set at $1.5M. For ease of calculation, we'll assume a total of 1,00,000 shares would be issued.</span>
            </div>
        """, unsafe_allow_html=True)


    st.markdown('<hr style="margin: 0.5em 0;">', unsafe_allow_html=True)
    col_1_1, col_1_2 = st.columns(2)

    with col_1_1:
        pre_money_valuation_usd_m = st.number_input("LeapX's Pre-Money Valuation (in $M)", min_value=2.5, value=5.0, step=0.5)
        pre_money_valuation_inr_cr = calculate_pre_money_valuation_inr(pre_money_valuation_usd_m)
        # st.write(f"Pre-Money Valuation in INR (Crore): ₹{pre_money_valuation_inr_cr:.2f} Cr")
    
    price_per_share_for_user = calculate_price_per_share_for_user(pre_money_valuation_usd_m)
    num_shares_allocated = int(investment_amount / price_per_share_for_user)


    col_2_1, col_2_2, col_2_3 = st.columns([2,0.2,2])
    with(col_2_1):

        pre_money_price_per_share = calculate_pre_money_price_per_share(pre_money_valuation_inr_cr)
        st.markdown(f"<span style='font-size: 0.8em;'>Pre-Money Valuation in INR (Crore): ₹{pre_money_valuation_inr_cr:.2f} Cr</span>", unsafe_allow_html=True)

        st.markdown(f"<span style='font-size: 0.8em;'>Pre-money Price per Share for future Investor: ₹{pre_money_price_per_share:.2f}</span>", unsafe_allow_html=True)

        st.markdown(f"<span style='font-size: 0.8em;'>Price per Share for YOU (basis valuation Cap): ₹{price_per_share_for_user}</span>", unsafe_allow_html=True)

        num_shares_allocated = int(investment_amount / price_per_share_for_user)
        st.markdown(f"<span style='font-size: 0.8em;'>Num of shares allocated to you (apprx): {num_shares_allocated}</span>", unsafe_allow_html=True)


    with col_2_3:
        pre_money_value_of_investment = num_shares_allocated * pre_money_price_per_share

        if investment_amount > 0:  # Prevent division by zero
            percentage_growth = ((pre_money_value_of_investment - investment_amount) / investment_amount) * 100
        else:
            percentage_growth = 0

        st.markdown(f"""
            <div style="text-align: center;">
                <span style='font-size: 1.2em;'><b>Pre-money value of YOUR Investment:</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center;">
                <span style='font-size: 2.5em;'>₹{pre_money_value_of_investment:.2f} <sup style='font-size: 0.5em; color: green;'>&#9650; {percentage_growth:.2f}%</sup></span>
            </div>
            """, unsafe_allow_html=True)


    st.markdown("""
    <style>
        .small-grey {
            text-align: center;
            font-size: 0.8em;
            color: grey;
        }
    </style>

    <p class="small-grey">Please Note - The equity would be transferred to you as soon as we raise our Pre-Seed/Seed round, in which we are aiming for a minimum valuation of $5M.
            However you won't be able to liquidate the equity until our Series A Round (which can be at anywhere between $20-50M valuation)</p>
    """, unsafe_allow_html=True)


    with st.expander("Click here to see what your investment would be worth after we raise our Series A Round."):
        series_a_valuation_m_usd = st.number_input("Predicted valuation at Series A (in $M)", min_value=15.0, value=20.0, step=1.0)

        # Assuming 1 USD = 83 INR for conversion, adjust if the rate changes
        series_a_valuation_inr = series_a_valuation_m_usd * MILLION * USD_TO_INR_RATE
        new_share_value_at_series_a = series_a_valuation_inr / TOTAL_SHARES_ISSUED

        # Display the jump in share value
        initial_share_value_used_for_allocation = price_per_share_for_user  # Assuming this is the price per share used for user's allocation

        st.markdown(f"""
            <div style="text-align: center; color: grey">
                <span style='font-size: 0.8em;'>The value of each of your shares would jump from ₹{initial_share_value_used_for_allocation:.2f} to ₹{new_share_value_at_series_a:.2f} at this Series A valuation.
            </div>
            """, unsafe_allow_html=True)




        investment_value_at_series_a = num_shares_allocated * new_share_value_at_series_a

        if investment_amount > 0:  # Prevent division by zero
            percentage_growth_series_a = ((investment_value_at_series_a - investment_amount) / investment_amount) * 100
        else:
            percentage_growth_series_a = 0

        # Display the investment value at Series A and the percentage growth
        st.markdown(f"""
            <div style="text-align: center;">
                <span style='font-size: 1em;'><b>and the total value of your investment would jump to -</b></span>
                <br>
                <span style='font-size: 2.5em;'>₹{investment_value_at_series_a:.2f} <sup style='font-size: 0.5em; color: green;'>&#9650; {percentage_growth_series_a:.2f}%</sup></span>
            </div>
            """, unsafe_allow_html=True)
        
        stages = ['Now', 'After Seed', 'After Series A']
        values = [investment_amount, pre_money_value_of_investment, investment_value_at_series_a]
        percentage_growth = ['', f'{percentage_growth:.2f}%', f'{percentage_growth_series_a:.2f}%']

        # Create the bar chart
        fig = go.Figure(data=[
            go.Bar(x=stages, y=values, text=values, textposition='auto', marker_color=['blue', 'orange', 'green'])
        ])

        # Customize the layout
        fig.update_layout(
            title='Investment Growth Stages',
            xaxis_title='Stage',
            yaxis_title='Value (₹)',
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            yaxis=dict(range=[0, max(values) * 1.2]),  # Set y-axis limit to 20% above the highest value
        )

        # Adding annotations for percentage growth with arrows
        annotations = []
        for i, value in enumerate(values):
            if i > 0:  # Skip the first bar ('Now') as it has no growth percentage
                annotations.append(dict(x=stages[i], y=value, xshift=-70, yshift=20,
                                        text=f"↑ {percentage_growth[i]}", showarrow=False,
                                        font=dict(color="green", size=12)))

        fig.update_layout(annotations=annotations)

        # Display the figure in Streamlit
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})


    faqs = [
        {
            "question": "By when are you planning to raise the Pre-Seed/Seed round?",
            "answer": "We are in active discussions with several Pre-Seed and Seed investors, receiving positive traction for our product. While no deal has been finalized yet, we are optimistic about securing a closure by August 2024 at the earliest."
        },
        {
            "question": "How is our price of share calculated?",
            "answer": "Your investment in us in this early stage would be considered to be a CCD (Compulsory Convertible Debenture), featuring a 25% discount witha  valuation cap of $2.5M. This means, irrespective of a higher valuation, the share value for you would be decided at either the valuation-25% or $2.5m, whichever is lower. For example, lets assume LeapX gets valued at 5M$ (₹ 41.5 Cr), and assuming that we have a total of 100000 shares; the share value for a normal investor would be ₹41.5 Cr/100000 which is ₹4150. The same share value for you would be calculated at the valuation cap which is $2.5M (₹20.75 Cr), and you would be given shares at ₹20.75 Cr/100000, which is ₹2075. That means you get higher number of shares than what a regular investor would get. For a deeper understanding, feel free to reach out to us."
        },
        {
            "question": "When will we be given the equity in the company, and when do we have an option to liquidate our equity/exit?",
            "answer": "Equity will be allocated to you as soon as we raise our Pre-Seed or Seed Round, at a discounted rate according to our CCD terms. An opportunity to exit or liquidate your equity will arise following our next investment round, which will be Series A."
        }
    ]

    # Customize these styles to adjust the font size of questions and answers
    question_style = "font-weight:bold; font-size:18px;"
    answer_style = "font-size:16px;"

    with st.expander("Frequently Asked Questions"):
        for faq in faqs:
            # Using markdown with unsafe_allow_html to allow for HTML content
            st.markdown(f"<div style='{question_style}'>{faq['question']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='{answer_style}'>{faq['answer']}</div>", unsafe_allow_html=True)
            # Adding a small separator for readability between FAQs
            st.markdown("---")

    # st.markdown(f"<span style='font-size: 0.9em;'>Pre-money value of YOUR Investment: ₹{pre_money_value_of_investment:.2f}</span>", unsafe_allow_html=True)

# if st.session_state['authenticated']:
#     main_app()
# else:
#     show_login_screen()