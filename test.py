import os, sys
st.write(sys.executable)
st.write("GOOGLE_API_KEY exists:", bool(os.getenv("GOOGLE_API_KEY")))
