#!/bin/bash

# ACE Intelligence System - Smoke Test Script
# Tests all main pages and critical resources for 200 status

echo "🚀 Starting smoke tests for ACE Intelligence System..."
echo "Testing server at: http://localhost:4321/ACE_Intelligence_System/"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
FAILURES=()

# Test function
test_url() {
    local url="$1"
    local name="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if curl -sSf "$url" -o /dev/null 2>/dev/null; then
        echo -e "${GREEN}✅ PASS${NC} - $name ($url)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC} - $name ($url)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        FAILURES+=("$name ($url)")
    fi
}

echo "📋 Testing main application pages..."

# Test main pages
test_url "http://localhost:4321/ACE_Intelligence_System/" "Homepage"
test_url "http://localhost:4321/ACE_Intelligence_System/about" "About Page"
test_url "http://localhost:4321/ACE_Intelligence_System/research" "Research Page (Redirect)"
test_url "http://localhost:4321/ACE_Intelligence_System/methodology" "Methodology Page"
test_url "http://localhost:4321/ACE_Intelligence_System/findings" "Findings Page"
test_url "http://localhost:4321/ACE_Intelligence_System/solution" "Solution Page"

echo ""
echo "🗂️ Testing stakeholder pages..."

test_url "http://localhost:4321/ACE_Intelligence_System/stakeholders/cuny" "CUNY Stakeholder Page"
test_url "http://localhost:4321/ACE_Intelligence_System/stakeholders/city" "City Stakeholder Page"

echo ""
echo "📊 Testing data and map resources..."

# Test critical data files
test_url "http://localhost:4321/ACE_Intelligence_System/data/insights/hourly_agg.csv" "Hourly Aggregated Data"
test_url "http://localhost:4321/ACE_Intelligence_System/data/insights/top_hotspots.csv" "Top Hotspots Data"

# Test embedded maps
test_url "http://localhost:4321/ACE_Intelligence_System/plots/enhanced_spatial_intelligence_map.html" "Enhanced Spatial Map"
test_url "http://localhost:4321/ACE_Intelligence_System/plots/cbd_congestion_pricing_map.html" "CBD Congestion Pricing Map"
test_url "http://localhost:4321/ACE_Intelligence_System/plots/cbd_spatial_map.html" "CBD Spatial Map"
test_url "http://localhost:4321/ACE_Intelligence_System/plots/exempt_spatial_scatter.html" "Exempt Vehicle Spatial Scatter"

echo ""
echo "⚙️ Testing additional resources..."

test_url "http://localhost:4321/ACE_Intelligence_System/resources" "Resources Page"

echo ""
echo "📱 Testing mobile navigation (checking if header loads)..."

# Test if main navigation elements are present (basic HTML structure test)
if curl -s "http://localhost:4321/ACE_Intelligence_System/" | grep -q "mobile-menu"; then
    echo -e "${GREEN}✅ PASS${NC} - Mobile navigation structure present"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ FAIL${NC} - Mobile navigation structure missing"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    FAILURES+=("Mobile navigation structure")
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
echo "🎯 Testing Route Analyzer component..."

# Test if Route Analyzer component loads
if curl -s "http://localhost:4321/ACE_Intelligence_System/" | grep -q "route-analyzer"; then
    echo -e "${GREEN}✅ PASS${NC} - Route Analyzer component present"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ FAIL${NC} - Route Analyzer component missing"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    FAILURES+=("Route Analyzer component")
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
echo "📋 Testing Three Datathon Questions section..."

if curl -s "http://localhost:4321/ACE_Intelligence_System/" | grep -q "Three Key Datathon Questions"; then
    echo -e "${GREEN}✅ PASS${NC} - Three Datathon Questions section present"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ FAIL${NC} - Three Datathon Questions section missing"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    FAILURES+=("Three Datathon Questions section")
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
echo "👥 Testing footer team credits..."

if curl -s "http://localhost:4321/ACE_Intelligence_System/" | grep -q "Jujutsu Query team"; then
    echo -e "${GREEN}✅ PASS${NC} - Team credits present in footer"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ FAIL${NC} - Team credits missing from footer"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    FAILURES+=("Team credits in footer")
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# Summary
echo ""
echo "======================================"
echo "🔍 SMOKE TEST SUMMARY"
echo "======================================"
echo -e "Total tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed tests: $PASSED_TESTS${NC}"
echo -e "${RED}Failed tests: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 ALL TESTS PASSED! The site is ready for presentation.${NC}"
    echo ""
    echo "✨ Site features verified:"
    echo "   • All main pages load (200 OK)"
    echo "   • Research page redirects properly"
    echo "   • Interactive maps are accessible"
    echo "   • Route Analyzer component is present"
    echo "   • CSV data files are served correctly"
    echo "   • Three Datathon Questions are displayed"
    echo "   • Team credits are in the footer"
    echo "   • Mobile navigation structure exists"
    echo ""
    echo "🚀 Ready for datathon presentation!"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Issues to address:${NC}"
    for failure in "${FAILURES[@]}"; do
        echo -e "   • ${RED}$failure${NC}"
    done
    echo ""
    echo "💡 Recommendation: Fix the failing tests before presenting"
    exit 1
fi