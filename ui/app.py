import streamlit as st
from models import LLMFactory, AgentManager
from tools import ToolsManager
from services import VectorStoreManager, OCRManager
from config import Config

# Initialize managers
Config.create_directories()
vectorstore_manager = VectorStoreManager()
ocr_manager = OCRManager()
tools_manager = ToolsManager()
agent_manager = AgentManager()

st.set_page_config(page_title="AI Agent", page_icon="🧠")
st.title("AI Agent")

class StreamlitUI:
    """Main Streamlit UI class with modular functions"""
    
    def __init__(self):
        self.vectorstore_manager = vectorstore_manager
        self.ocr_manager = ocr_manager
        self.tools_manager = tools_manager
        self.agent_manager = agent_manager
    
    def render_model_selection(self):
        """Render model selection buttons and API key input"""
        st.title("Choose LLM Model")
        
        # Model selection buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Llama"):
                st.session_state.selected_model = "llama"
                st.session_state.llm = LLMFactory.create_llm("llama")
                st.success("Llama model loaded.")
        
        with col2:
            if st.button("Gemini"):
                st.session_state.selected_model = "gemini"
        
        # Gemini API key form
        self._render_gemini_api_form()
        
        # Show active model info
        if "llm" in st.session_state:
            st.info(f"Current model: {st.session_state.selected_model}")
    
    def _render_gemini_api_form(self):
        """Render Gemini API key input form"""
        if st.session_state.get("selected_model") == "gemini":
            with st.form("gemini_key_form"):
                google_api_key = st.text_input("Enter Google API Key (for Gemini)", type="password")
                submitted = st.form_submit_button("Load Gemini")
                if submitted:
                    if google_api_key:
                        st.session_state.llm = LLMFactory.create_llm("gemini", google_api_key)
                        st.success("Gemini model loaded.")
                    else:
                        st.warning("Please enter your Google API key to use Gemini.")
    
    def render_document_upload(self):
        """Render document upload section"""
        uploaded_file = st.file_uploader("Upload a new document (PDF or HTML)", type=["pdf", "html"])
        
        if st.button("Add document"):
            if uploaded_file is not None:
                result = self._process_uploaded_document(uploaded_file)
                st.success(result)
            else:
                st.error("Please upload a valid PDF or HTML file.")
    
    def _process_uploaded_document(self, uploaded_file):
        """Process and save uploaded document to vectorstore"""
        save_path = f"{Config.UPLOAD_DIR}/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        
        return self.vectorstore_manager.add_document_to_vectorstore(save_path)
    
    def render_vectorstore_reset(self):
        """Render vectorstore reset button"""
        if st.button("Reset Vectorstore"):
            result = self.vectorstore_manager.reset_vectorstore()
            st.warning(result)
    
    def render_vectorstore_controls(self):
        """Render complete vectorstore management section"""
        st.title("Vectorstore Controls")
        self.render_document_upload()
        self.render_vectorstore_reset()
    
    def render_sidebar(self):
        """Render complete sidebar with model selection and document management"""
        with st.sidebar:
            self.render_model_selection()
        
        with st.sidebar:
            self.render_vectorstore_controls()
    
    def render_chat_instructions(self):
        """Render chat agent instructions and capabilities"""
        st.markdown("""
        **Talk to Your AI Assistant**

        This agent is capable of:
        - 📄 Retrieving data from **PDF** and **HTML** documents stored in a vector store
        - 🌤️ Providing **live weather** info
        - 🧮 Performing **mathematical calculations**
        - 📚 Searching **Wikipedia** for real-world knowledge

        Just type your question and let the agent figure it out!
        """)
    
    def get_chat_inputs(self):
        """Get user inputs for chat (query and optional image)"""
        user_query = st.text_input("Enter your question:")
        uploaded_image = st.file_uploader("Optional: Upload an image", type=["png", "jpg", "jpeg"])
        return user_query, uploaded_image
    
    def process_chat_query(self, user_query, uploaded_image):
        """Process chat query and return response"""
        full_query = user_query
        
        # Add OCR context if image is uploaded
        if uploaded_image is not None:
            extracted_text = self.ocr_manager.process_uploaded_image(uploaded_image)
            full_query += f"\n\nContext from image:\n{extracted_text}"
        
        # Get response from agent
        llm = st.session_state.llm
        tools = self.tools_manager.get_all_tools()
        agent = self.agent_manager.create_react_agent(llm, tools)
        thread_id = "default_user"  # Since no auth, use default
        
        return self.agent_manager.get_agent_response(agent, full_query, thread_id)
    
    def handle_chat_submission(self, user_query, uploaded_image):
        """Handle chat form submission with validation and error handling"""
        if not user_query:
            st.warning("Please enter a question.")
            return
        
        if "llm" not in st.session_state:
            st.error("Please select a model first.")
            return
        
        try:
            answer = self.process_chat_query(user_query, uploaded_image)
            st.success("Answer:")
            st.markdown(answer.replace("$", "\\$"))
        except Exception as e:
            st.error(f"Error: {e}")
    
    def render_chat_tab(self):
        """Render complete chat agent tab"""
        st.subheader("Chat Agent")
        
        self.render_chat_instructions()
        user_query, uploaded_image = self.get_chat_inputs()
        
        if st.button("Submit Query", key="chat_query"):
            self.handle_chat_submission(user_query, uploaded_image)
    
    def get_csv_inputs(self):
        """Get CSV file upload and query input"""
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        user_query = st.text_input("Ask a question about the data:")
        return uploaded_file, user_query
    
    def display_csv_preview(self, uploaded_file):
        """Display CSV file preview"""
        df = self.vectorstore_manager.load_dataframe(uploaded_file)
        st.success("CSV file loaded successfully!")
        st.dataframe(df.head())
        return df
    
    def process_csv_query(self, df, user_query):
        """Process CSV query using DataFrame agent"""
        if "llm" not in st.session_state:
            st.error("Please select a model first.")
            return
        
        try:
            answer = self.agent_manager.query_dataframe(
                st.session_state.llm, df, user_query
            )
            st.success("Answer:")
            st.markdown(answer, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error querying the data: {e}")
    
    def handle_csv_query_submission(self, df, user_query):
        """Handle CSV query submission with validation"""
        if user_query.strip():
            self.process_csv_query(df, user_query)
        else:
            st.warning("Please enter a question to query.")
    
    def render_csv_tab(self):
        """Render complete CSV query tab"""
        st.subheader("Query CSV")
        
        uploaded_file, user_query = self.get_csv_inputs()
        
        if uploaded_file:
            df = self.display_csv_preview(uploaded_file)
            
            if st.button("Query DataFrame"):
                self.handle_csv_query_submission(df, user_query)
    
    def render_main_tabs(self):
        """Render main application tabs"""
        tab1, tab2 = st.tabs(["Chat Agent", "Query CSV"])
        
        with tab1:
            self.render_chat_tab()
        
        with tab2:
            self.render_csv_tab()
    
    def run(self):
        """Main application runner"""
        self.render_sidebar()
        self.render_main_tabs()

# Run the application
if __name__ == "__main__":
    app = StreamlitUI()
    app.run()