import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Initialize the GenAI client
client = genai.Client(api_key="AIzaSyBJ-DRlRBbia5djwgT2ePHWWCc3o71KVII")

# Streamlit UI
st.title("Generate Content with GenAI")
st.write("Choose to generate content using either a text prompt or an uploaded image.")

# Tabs for functionality
tab1, tab2 = st.tabs(["Text-to-Image", "Image-to-Image"])

# Text-to-Image Generation
with tab1:
    st.header("Text-to-Image Generation")
    prompt = st.text_input("Enter your prompt:", "Generate an image of a cat wearing a hat")

    if st.button("Generate from Text"):
        with st.spinner("Generating content..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

        # Process the response
        text_output = None
        image = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_output = part.text
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))

        # Display the results
        if text_output:
            st.subheader("Generated Text:")
            st.write(text_output)

        if image:
            st.subheader("Generated Image:")
            st.image(image, caption="Generated Image", use_column_width=True)

# Image-to-Image Generation
with tab2:
    st.header("Image-to-Image Generation")
    uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    text_input = st.text_input("Enter a description for the transformation:", "Remove the text and choose trending colors.")

    if st.button("Generate from Image"):
        if uploaded_image is not None:
            with st.spinner("Generating content..."):
                # Open the uploaded image
                image = Image.open(uploaded_image)

                # Generate content using GenAI
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[text_input, image],
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

            # Process the response
            text_output = None
            transformed_image = None
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    text_output = part.text
                elif part.inline_data is not None:
                    transformed_image = Image.open(BytesIO(part.inline_data.data))

            # Display the results
            if text_output:
                st.subheader("Generated Text:")
                st.write(text_output)

            if transformed_image:
                st.subheader("Transformed Image:")
                st.image(transformed_image, caption="Transformed Image", use_column_width=True)
        else:
            st.error("Please upload an image to proceed.")