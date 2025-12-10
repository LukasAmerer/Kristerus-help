"""
Azure AD Authentication using MSAL for Streamlit
"""
import os
import msal
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class AzureADAuth:
    """Handles Microsoft Azure AD authentication"""
    
    def __init__(self):
        """Initialize MSAL configuration"""
        self.client_id = os.getenv("AZURE_AD_CLIENT_ID")
        self.tenant_id = os.getenv("AZURE_AD_TENANT_ID")
        self.client_secret = os.getenv("AZURE_AD_CLIENT_SECRET")
        self.redirect_uri = os.getenv("AZURE_AD_REDIRECT_URI", "http://localhost:8501")
        
        # Use "common" to allow any Azure AD tenant + Microsoft accounts (fixes AADSTS50020)
        # This supports federated identity providers (like university SSO)
        self.authority = "https://login.microsoftonline.com/common"
        self.scope = ["User.Read"]
        
        # Check if credentials are configured
        if not all([self.client_id, self.tenant_id, self.client_secret]):
            print("⚠️ Azure AD credentials not configured. Using fallback authentication.")
            self.enabled = False
        else:
            self.enabled = True
            print("✅ Azure AD authentication enabled")
    
    def get_auth_url(self):
        """Get the authorization URL for user to login"""
        if not self.enabled:
            return None
        
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        # Generate auth URL with prompt to always show account picker
        auth_url = app.get_authorization_request_url(
            scopes=self.scope,
            redirect_uri=self.redirect_uri,
            prompt="select_account"  # Force account picker to appear
        )
        
        return auth_url
    
    def get_token_from_code(self, auth_code):
        """Exchange authorization code for access token"""
        if not self.enabled:
            return None
        
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_by_authorization_code(
            auth_code,
            scopes=self.scope,
            redirect_uri=self.redirect_uri
        )
        
        return result
    
    def get_user_info(self, access_token):
        """Get user information from Microsoft Graph API"""
        import requests
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        return None

# Global auth instance
azure_auth = AzureADAuth()


def login_with_azure():
    """Handle Azure AD login flow"""
    
    # Whitelist of allowed email addresses
    ALLOWED_EMAILS = [
        "alexander.spreckelsen@unisg.ch",
        "lukas.amerer@student.unisg.ch"
    ]
    
    # Check if we have an auth code in URL parameters
    query_params = st.query_params
    
    if "code" in query_params:
        # We got redirected back with auth code
        auth_code = query_params["code"]
        
        # Exchange code for token
        with st.spinner("🔐 Authenticating with Microsoft..."):
            result = azure_auth.get_token_from_code(auth_code)
            
            if "access_token" in result:
                # Get user info
                user_info = azure_auth.get_user_info(result["access_token"])
                
                if user_info:
                    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
                    user_name = user_info.get("displayName")
                    
                    # Check if email is in whitelist
                    if user_email and user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
                        # Store in session
                        st.session_state.logged_in = True
                        st.session_state.user_email = user_email
                        st.session_state.user_name = user_name
                        st.session_state.access_token = result["access_token"]
                        
                        # Clear query params
                        st.query_params.clear()
                        
                        st.success(f"✅ Welcome, {user_name}!")
                        st.rerun()
                    else:
                        # Not authorized
                        st.query_params.clear()
                        st.error(f"❌ Access Denied: {user_email} is not authorized to access this application.")
                        st.info("Only the following email addresses are allowed:\n\n" + "\n".join([f"• {email}" for email in ALLOWED_EMAILS]))
                else:
                    st.error("Failed to get user information")
            else:
                st.error(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
    
    else:
        # Simple login page title
        st.markdown(
            """
            <div style="text-align: center; padding: 20px 0 40px 0;">
                <h1 style="color: #2A996F; margin-bottom: 8px;">Login</h1>
                <p style="color: #6c757d; font-size: 14px;">Access the Research Assistant</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Traditional login form
            st.markdown("<h3 style='text-align: center; color: #2A996F; margin-bottom: 20px;'>Login</h3>", unsafe_allow_html=True)
            
            email = st.text_input("Email", placeholder="your.email@example.com", key="login_email_field")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password_field")
            
            if st.button("🔓 Sign In", use_container_width=True, type="primary"):
                # Simple validation for demo
                ALLOWED_EMAILS = [
                    "alexander.spreckelsen@unisg.ch",
                    "lukas.amerer@student.unisg.ch"
                ]
                
                if email and password:
                    if email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split('@')[0].replace('.', ' ').title()
                        st.success(f"✅ Welcome, {st.session_state.user_name}!")
                        st.rerun()
                    else:
                        st.error(f"❌ Access Denied: {email} is not authorized.")
                        st.info("Only the following emails are allowed:\n\n" + "\n".join([f"• {e}" for e in ALLOWED_EMAILS]))
                else:
                    st.error("Please enter both email and password.")
            
            # Divider
            st.markdown(
                """
                <div style="text-align: center; margin: 30px 0 20px 0;">
                    <span style="color: #6c757d; font-size: 14px;">OR</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Microsoft sign-in option
            if azure_auth.enabled:
                # Get auth URL
                auth_url = azure_auth.get_auth_url()
                
                # Official Microsoft Sign-in Button with Logo
                st.markdown(
                    f"""
                    <style>
                    .ms-signin-btn {{
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        width: 100%;
                        padding: 10px 12px;
                        background-color: #FFFFFF;
                        border: 1px solid #8C8C8C;
                        border-radius: 2px;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        font-size: 15px;
                        font-weight: 600;
                        color: #5E5E5E;
                        text-decoration: none;
                        cursor: pointer;
                        transition: all 0.2s ease;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .ms-signin-btn:hover {{
                        background-color: #F0F0F0;
                        border-color: #5E5E5E;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    }}
                    .ms-signin-btn:active {{
                        background-color: #E5E5E5;
                    }}
                    .ms-logo {{
                        width: 21px;
                        height: 21px;
                        margin-right: 12px;
                    }}
                    </style>
                    
                    <a href="{auth_url}" class="ms-signin-btn">
                        <svg class="ms-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21 21">
                            <rect x="1" y="1" width="9" height="9" fill="#f25022"/>
                            <rect x="1" y="11" width="9" height="9" fill="#00a4ef"/>
                            <rect x="11" y="1" width="9" height="9" fill="#7fba00"/>
                            <rect x="11" y="11" width="9" height="9" fill="#ffb900"/>
                        </svg>
                        Sign in with Microsoft
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ Azure AD is not configured. Please add credentials to .env file.")
                st.code("""
AZURE_AD_CLIENT_ID=<your-client-id>
AZURE_AD_TENANT_ID=<your-tenant-id>
AZURE_AD_CLIENT_SECRET=<your-client-secret>
AZURE_AD_REDIRECT_URI=http://localhost:8501
                """, language="bash")


def logout_azure():
    """Handle Azure AD logout"""
    st.markdown(
        """
        <style>
        .logout-container {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            text-align: center;
            margin: 40px auto;
            max-width: 600px;
        }
        .logout-title {
            font-size: 36px;
            font-weight: 800;
            color: #2A996F;
            margin-bottom: 16px;
        }
        .logout-subtitle {
            font-size: 16px;
            color: #6c757d;
            margin-bottom: 30px;
        }
        .user-badge {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin: 20px 0;
        }
        .user-icon {
            font-size: 48px;
            margin-bottom: 12px;
        }
        </style>
        
        <div class="logout-container">
            <div class="user-icon">👤</div>
            <div class="logout-title">You're Signed In</div>
            <div class="logout-subtitle">Successfully authenticated</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if "user_name" in st.session_state:
            st.markdown(
                f"""
                <div class="user-badge">
                    <div style="font-size: 20px; font-weight: 700; color: #2A996F; margin-bottom: 8px;">
                        {st.session_state.user_name}
                    </div>
                    <div style="font-size: 14px; color: #6c757d;">
                        {st.session_state.user_email}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            """
            <style>
            .stButton>button {
                background: linear-gradient(90deg, #dc3545 0%, #c82333 100%);
                color: white;
                font-size: 16px;
                font-weight: 600;
                padding: 14px 28px;
                border: none;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(220,53,69,0.3);
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 24px rgba(220,53,69,0.4);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🚪 Sign Out", use_container_width=True, type="primary"):
            # Clear session
            st.session_state.logged_in = False
            st.session_state.pop("user_email", None)
            st.session_state.pop("user_name", None)
            st.session_state.pop("access_token", None)
            
            st.success("✅ Successfully signed out!")
            st.rerun()
