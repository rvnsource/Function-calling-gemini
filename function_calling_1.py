import vertexai
import os
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    GenerationConfig,
    Part,
    Tool,
)

# Vertex AI Initialization
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ravi/.config/gcloud/genai-434714-5b6098f8999f.json"
PROJECT_ID = "genai-434714"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Function Declarations
get_product_info = FunctionDeclaration(
    name="get_product_info",
    description="Get the stock amount and identifier for a given product",
    parameters={
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "Product name"}
        },
    },
)

# Initialize Retail Tool
retail_tool = Tool(
    function_declarations=[get_product_info],
)

# Initialize the Model
model = GenerativeModel(
    "gemini-1.5-pro-001",
    generation_config=GenerationConfig(temperature=0),
    tools=[retail_tool],
)

chat = model.start_chat()

# Function Call and Immediate Response Handling
def handle_product_info(product_name):
    """Simulate an API response after a function call."""
    # Simulate sending a prompt to the LLM
    prompt = f"Do you have the {product_name} in stock?"
    response = chat.send_message(prompt)

    # Ensure the function call response immediately follows
    print(response.candidates[0].content.parts[0])

    # Synthetic API response
    api_response = {"sku": "GA04834-US", "in_stock": "yes"}

    # Send the function response
    function_response = Part.from_function_response(
        name="get_product_info",
        response={"content": api_response},
    )
    
    # Send the response to the model
    final_response = chat.send_message(function_response)
    print(final_response.text)

# Call the Function and Provide the Response
handle_product_info("Pixel 8 Pro")
handle_product_info("Pixel 8")
