import streamlit as st
import urllib.parse

def generate_amazon_url(supplement):
    encoded_supplement = urllib.parse.quote(supplement)
    return f"https://www.amazon.com/s?k={encoded_supplement}"

def main():
    st.title("Supplement Amazon Links")

    supplements = [
        "Vitamin D3",
        "Omega-3 Fish Oil",
        "Magnesium Glycinate",
        "Vitamin B12",
        "Zinc",
        "Probiotics",
        "Vitamin C",
        "Turmeric Curcumin",
        "Calcium",
        "Iron",
        "Coenzyme Q10 (CoQ10)",
        "Glucosamine",
        "Melatonin",
        "Ashwagandha",
        "Creatine Monohydrate"
    ]

    st.subheader("Amazon Links:")
    for supplement in supplements:
        url = generate_amazon_url(supplement)
        st.markdown(f"- [{supplement}]({url})")

if __name__ == "__main__":
    main()