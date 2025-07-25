"""
Test script to verify BEP Agent installation and configuration.
"""

import os
import sys
from config import Config

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("Testing dependencies...")
    
    required_packages = [
        'openai', 'faiss', 'langchain', 'sentence_transformers',
        'docx', 'streamlit', 'dotenv', 'numpy', 'pandas', 'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            elif package == 'faiss':
                import faiss
            elif package == 'sklearn':
                import sklearn
            elif package == 'sentence_transformers':
                import sentence_transformers
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed successfully!")
        return True

def test_configuration():
    """Test configuration and environment setup."""
    print("\nTesting configuration...")
    
    try:
        # Test config loading
        Config.validate_config()
        print("✅ Configuration loaded successfully")
        
        # Check API key
        if Config.USE_LOCAL_EMBEDDINGS:
            print("✅ Using local embeddings (no API key required)")
        elif Config.OPENAI_API_KEY:
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured")
            print("   Set OPENAI_API_KEY in .env file or enable USE_LOCAL_EMBEDDINGS")
        
        # Check directories
        directories = [Config.BEP_SAMPLES_DIR, Config.NEW_PROJECT_DIR, Config.VECTOR_STORE_PATH]
        for directory in directories:
            if os.path.exists(directory):
                print(f"✅ Directory exists: {directory}")
            else:
                print(f"❌ Directory missing: {directory}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def test_sample_documents():
    """Test if sample BEP documents are available."""
    print("\nTesting sample documents...")
    
    if not os.path.exists(Config.BEP_SAMPLES_DIR):
        print(f"❌ Sample directory not found: {Config.BEP_SAMPLES_DIR}")
        return False
    
    sample_files = [f for f in os.listdir(Config.BEP_SAMPLES_DIR) if f.endswith('.docx')]
    
    if sample_files:
        print(f"✅ Found {len(sample_files)} sample BEP documents:")
        for file in sample_files:
            print(f"   - {file}")
        return True
    else:
        print("⚠️  No sample BEP documents found")
        print(f"   Please add .docx files to {Config.BEP_SAMPLES_DIR}")
        return False

def test_basic_functionality():
    """Test basic functionality without full initialization."""
    print("\nTesting basic functionality...")
    
    try:
        from document_loader import DocumentLoader
        from vector_store import VectorStore
        from outline_generator import OutlineGenerator
        
        # Test document loader
        loader = DocumentLoader()
        print("✅ DocumentLoader initialized")
        
        # Test vector store (without building index)
        vector_store = VectorStore()
        print("✅ VectorStore initialized")
        
        # Test outline generator (requires API key)
        if Config.OPENAI_API_KEY:
            outline_gen = OutlineGenerator()
            print("✅ OutlineGenerator initialized")
        else:
            print("⚠️  OutlineGenerator requires OpenAI API key")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🏗️ BEP Agent Installation Test")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Sample Documents", test_sample_documents),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! BEP Agent is ready to use.")
        print("Run 'streamlit run main.py' to start the application.")
    else:
        print("⚠️  Some tests failed. Please address the issues above.")
        print("Check the README.md for setup instructions.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
