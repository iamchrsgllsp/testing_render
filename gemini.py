import google.generativeai as genai
from typing import Optional, Dict, Any
import os


def generate_with_gemini(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 2048,
) -> Dict[Any, Any]:
    """
    Generate text using Google's Gemini API.

    Args:
        prompt (str): The input text prompt
        api_key (str, optional): Gemini API key. If not provided, will look for GOOGLE_API_KEY env variable
        model (str): Model to use (default: 'gemini-pro')
        temperature (float): Controls randomness (0.0-1.0)
        top_p (float): Controls diversity via nucleus sampling (0.0-1.0)
        max_tokens (int): Maximum number of tokens to generate

    Returns:
        dict: Response from the Gemini API

    Raises:
        ValueError: If no API key is provided or found in environment
        Exception: For API errors or other issues
    """
    # Get API key from args or environment
    api_key = "AIzaSyC_wJB2VKm4bN-5-_VDwjf2zv8-tv9N3i8"
    if not api_key:
        raise ValueError(
            "Gemini API key must be provided or set as GOOGLE_API_KEY environment variable"
        )

    # Configure the Gemini API
    genai.configure(api_key=api_key)

    # Set up the model
    model = genai.GenerativeModel(model_name=model)

    try:
        # Generate the response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature, top_p=top_p, max_output_tokens=max_tokens
            ),
        )

        return {
            "text": response.text,
            "prompt_feedback": response.prompt_feedback,
            "candidates": response.candidates,
        }

    except Exception as e:
        raise Exception(f"Error generating content with Gemini: {str(e)}")
