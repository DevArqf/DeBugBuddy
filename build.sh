set -e

echo "🐛 DeBugBuddy Build Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_step() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_step "Cleaning old builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
print_success "Cleaned old builds"

print_step "Checking requirements..."
if ! command -v python &> /dev/null; then
    print_error "Python not found"
    exit 1
fi

if ! python -c "import setuptools" &> /dev/null; then
    print_error "setuptools not installed"
    exit 1
fi

if ! python -c "import wheel" &> /dev/null; then
    print_warning "wheel not installed, installing..."
    pip install wheel
fi

if ! command -v twine &> /dev/null; then
    print_warning "twine not installed, installing..."
    pip install twine
fi

print_success "All requirements met"

if [ -d "tests" ]; then
    print_step "Running tests..."
    if command -v pytest &> /dev/null; then
        pytest || {
            print_error "Tests failed"
            exit 1
        }
        print_success "Tests passed"
    else
        print_warning "pytest not found, skipping tests"
    fi
fi

print_step "Building package..."
python setup.py sdist bdist_wheel
print_success "Package built"

print_step "Checking package..."
twine check dist/*
print_success "Package check passed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Package Information"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh dist/
echo ""

echo "What would you like to do?"
echo "  1) Test locally (pip install dist/*.whl)"
echo "  2) Upload to TestPyPI"
echo "  3) Upload to PyPI"
echo "  4) Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        print_step "Installing locally..."
        pip uninstall debugbuddy -y 2>/dev/null || true
        pip install dist/*.whl
        print_success "Installed locally"
        echo ""
        echo "Test it:"
        echo "  db"
        echo "  db --version"
        echo "  db explain \"test error\""
        ;;
    2)
        print_step "Uploading to TestPyPI..."
        twine upload --repository testpypi dist/*
        print_success "Uploaded to TestPyPI"
        echo ""
        echo "Test it:"
        echo "  pip install --index-url https://test.pypi.org/simple/ debugbuddy"
        ;;
    3)
        print_warning "Are you sure you want to upload to PyPI?"
        read -p "This cannot be undone! [y/N]: " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            print_step "Uploading to PyPI..."
            twine upload dist/*
            print_success "Uploaded to PyPI"
            echo ""
            echo "🎉 DeBugBuddy is now live on PyPI!"
            echo ""
            echo "Install it:"
            echo "  pip install debugbuddy"
            echo ""
        else
            print_warning "Upload cancelled"
        fi
        ;;
    4)
        print_success "Build complete"
        ;;
    *)
        print_error "Invalid choice"
        ;;
esac

echo ""
print_success "Done! 🎉"