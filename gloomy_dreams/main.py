from nicegui import ui
from datetime import datetime
from gloomy_dreams.graph import create_finance_graph
from gloomy_dreams.ui import render_ui
import asyncio
import os

# --- Setup Graph and export visualization ---
# This requires Graphviz to be installed and in your system's PATH
graph = create_finance_graph()


def export_graph_image(graph_obj, output_path: str = "static/graph_structure.png"):
    """Exports the LangGraph structure as a PNG image."""

    if os.path.exists(output_path):
        print("file already present")
        return
    try:
        # Ensure the graphviz library is available and the graph can be rendered
        if hasattr(graph_obj, 'get_graph'):
            g = graph_obj.get_graph()
            # check if draw_png method exists
            if hasattr(g, 'draw_png'):
                 g.draw_png(output_path)  # Requires Graphviz executable
                 print(f"[INFO] Graph structure image saved to {output_path}")
            else:
                 print("[ERROR] Graph object does not have 'draw_png' method. Graphviz might not be fully integrated.")
        else:
            print("[ERROR] Graph object does not have 'get_graph' method. Cannot export image.")

    except FileNotFoundError:
        print("[ERROR] Graphviz executable not found. Please install Graphviz and ensure it's in your system's PATH.")
        print("Installation instructions: https://graphviz.org/download/")
    except Exception as e:
        print(f"[ERROR] Failed to generate graph image: {e}")


# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Attempt to export the graph image
export_graph_image(graph)


# --- Define sections ---
sections = ["Sentiment Analysis", "Project Details"]
current_section = "Sentiment Analysis"  # Default page

# --- Placeholder objects for dynamic content ---
# These will hold the actual UI elements created during rendering
content_area = None
# Variables within sections are now defined inside render_current_section to avoid scope issues
# ticker_input = None
# analyze_button = None
# spinner = None
# loading_text = None
# result_container = None


# --- Function to handle section switch ---
def switch_section(section: str):
    """Switches the currently displayed section."""
    global current_section
    if current_section != section: # Only switch if different
        current_section = section
        if content_area: # Clear only if content_area is already defined
            content_area.clear()
        render_current_section()


# --- Function to render content based on active section ---
def render_current_section():
    """Renders the UI for the current active section within the content_area."""
    # Define section-specific variables here
    section_ticker_input = None
    section_analyze_button = None
    section_spinner = None
    section_loading_text = None
    section_result_container = None

    if current_section == "Sentiment Analysis":
        with content_area:
            with ui.card().classes('w-full p-4 shadow-md'): # Use a card for better visual grouping
                ui.label("Agentic AI: Financial News Sentiment Analyzer").classes("text-2xl font-bold mb-4 text-center")

                with ui.column().classes('w-full items-center gap-4'): # Column for input and button
                    section_ticker_input = ui.input("Enter stock ticker", placeholder="e.g., AAPL").classes('w-full max-w-sm') # Constrain width
                    section_analyze_button = ui.button("Analyze", color="primary").classes('w-full max-w-sm') # Constrain width

                with ui.column().classes('w-full items-center mt-4'): # Column for loading indicators
                    section_spinner = ui.spinner(size='lg')
                    section_spinner.visible = False

                    section_loading_text = ui.label("").classes("text-md italic text-gray-500")
                    section_loading_text.visible = False

                # Container for the detailed results from render_ui
                section_result_container = ui.column().classes("w-full mt-4 p-4 border rounded-lg bg-blue-50") # Added border, padding, background

                # --- Hook up Analyze button for this section ---
                # Use the section-specific variables and pass them to run_pipeline
                section_analyze_button.on("click",
                                         lambda: run_pipeline(
                                             section_ticker_input.value,
                                             section_spinner,
                                             section_loading_text,
                                             section_result_container
                                         ))


    elif current_section == "Project Details":
        with content_area:
            with ui.card().classes('w-full p-6 shadow-md items-center text-center'): # Card with padding and centered content
                ui.label("About This Project").classes("text-xl font-bold mb-4")

                ui.label("""
This application uses an agentic AI system built with LangGraph and NiceGUI to perform financial news sentiment analysis.

It retrieves real-world financial news, summarizes using local LLMs,
classifies sentiment, and presents a clean, dynamic UI.
""").classes("text-sm max-w-prose mx-auto q-mb-md") # Added max-width, auto margins for centering, margin-bottom

                ui.label("Workflow Diagram").classes("text-md font-semibold mt-6 mb-4") # Added margins
                # Ensure image path is correct and image exists
                if os.path.exists('static/graph_structure.png'):
                     ui.image('static/graph_structure.png').classes('w-full max-w-xl rounded-lg shadow mx-auto') # Constrain width, center image
                else:
                     ui.label("Workflow diagram not available. Please ensure Graphviz is installed and the image is generated correctly.").classes("text-red-500")


                with ui.row().classes('mt-6 gap-4 justify-center'): # Added margin-top, gap, center buttons
                    ui.button("🌐 GitHub", on_click=lambda: ui.run_javascript(
                        "window.open('https://github.com/pankajti/gloomy-dreams', '_blank')"))

                    ui.button("🔗 LinkedIn", on_click=lambda: ui.run_javascript("window.open('https://www.linkedin.com/in/pankajti/', '_blank')"))



# --- Async function for pipeline ---
# Modified to accept specific UI elements for the active section
async def run_pipeline(ticker: str, spinner_element: ui.spinner, loading_text_element: ui.label, result_container_element: ui.column):
    if result_container_element:
        result_container_element.clear() # Clear previous results

    if spinner_element:
        spinner_element.visible = True
    if loading_text_element:
        loading_text_element.text = "Loading analysis results..."
        loading_text_element.visible = True

    ui.notify(f"Analyzing sentiment for {ticker}...", type="info")

    # Short sleep to allow UI to update before blocking call
    await asyncio.sleep(0.1)
    state = {
        "ticker": ticker,
        "retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        # Run the potentially blocking graph invocation in a separate thread
        result = await asyncio.to_thread(graph.invoke, state)

        if spinner_element:
            spinner_element.visible = False
        if loading_text_element:
            loading_text_element.visible = False

        if result_container_element:
            with result_container_element:
                # render_ui should add elements within this context
                render_ui(result)
        ui.notify("Analysis complete!", type="positive")

    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}")
        if spinner_element:
            spinner_element.visible = False
        if loading_text_element:
            loading_text_element.text = f"Error: {e}"
            loading_text_element.visible = True
        ui.notify(f"Analysis failed: {e}", type="negative")


# --- Layout UI ---
with ui.row().classes("w-full h-screen no-wrap"): # Use no-wrap to prevent sidebar wrapping
    # --- Sidebar: Vertical Menu ---
    # Fixed width for sidebar, allow content area to take remaining space
    with ui.column().classes("w-1/5 min-w-[200px] bg-gray-100 p-4 gap-4 items-start flex-shrink-0"): # Added min-width and flex-shrink
        ui.label("Gloomy Dreams").classes("text-lg font-bold mb-4")

        for section in sections:
            ui.button(section, on_click=lambda s=section: switch_section(s)).classes('w-full text-left')

    # --- Content Area: Dynamic ---
    # Use a column to stack content, allow it to grow
    with ui.column().classes("w-4/5 p-6 gap-4 items-center flex-grow") as content_area: # Added flex-grow
        # Initial rendering of the default section
        render_current_section()


# --- Run app ---
ui.run(title="LangGraph Finance Sentiment App")