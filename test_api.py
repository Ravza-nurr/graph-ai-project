import requests
import json

# Test 1: Upload titanic.csv
print("=" * 50)
print("TEST 1: Uploading titanic.csv")
print("=" * 50)

with open('data/samples/titanic.csv', 'rb') as f:
    files = {'file': ('titanic.csv', f, 'text/csv')}
    response = requests.post('http://localhost:8000/upload', files=files)
    
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    file_id = data['file_id']
    print(f"✅ Upload successful!")
    print(f"File ID: {file_id}")
    print(f"Rows: {data['metadata']['num_rows']}")
    print(f"Columns: {data['metadata']['num_columns']}")
    print(f"Numeric columns: {data['metadata']['numeric_columns'][:3]}")
    
    # Check AI recommendations
    if 'ai_recommendations' in data['metadata']:
        ai_rec = data['metadata']['ai_recommendations']
        print(f"\n🤖 AI Studio Status: {'Enabled ✅' if ai_rec.get('available') else 'Disabled ❌'}")
        if ai_rec.get('recommendations'):
            print(f"AI Recommendations: {len(ai_rec['recommendations'])} charts suggested")
            for i, rec in enumerate(ai_rec['recommendations'][:3], 1):
                print(f"  {i}. {rec.get('type', 'unknown')} - {rec.get('reason', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("TEST 2: Generating BAR Chart")
    print("=" * 50)
    
    # Test 2: Generate bar chart
    chart_request = {
        "file_id": file_id,
        "chart_type": "bar",
        "x_column": "Pclass",
        "y_columns": None
    }
    
    response = requests.post('http://localhost:8000/generate-chart', json=chart_request)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Bar chart generated!")
        print(f"Chart URL: {data['chart_url']}")
        print(f"Caption: {data['caption'][:100]}...")
    else:
        print(f"❌ Error: {response.text}")
    
    print("\n" + "=" * 50)
    print("TEST 3: Generating LINE Chart")  
    print("=" * 50)
    
    # Test 3: Generate line chart
    chart_request = {
        "file_id": file_id,
        "chart_type": "line",
        "x_column": "PassengerId",
        "y_columns": ["Age", "Fare"]
    }
    
    response = requests.post('http://localhost:8000/generate-chart', json=chart_request)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Line chart generated!")
        print(f"Chart URL: {data['chart_url']}")
        print(f"Caption: {data['caption'][:100]}...")
    else:
        print(f"❌ Error: {response.text}")
    
    print("\n" + "=" * 50)
    print("TEST 4: Generating SCATTER Chart")
    print("=" * 50)
    
    # Test 4: Generate scatter chart
    chart_request = {
        "file_id": file_id,
        "chart_type": "scatter",
        "x_column": "Age",
        "y_columns": ["Fare"],
        "color_column": "Sex"
    }
    
    response = requests.post('http://localhost:8000/generate-chart', json=chart_request)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Scatter chart generated!")
        print(f"Chart URL: {data['chart_url']}")
        print(f"Caption: {data['caption'][:100]}...")
    else:
        print(f"❌ Error: {response.text}")
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETED!")
    print("=" * 50)
    
else:
    print(f"❌ Upload failed: {response.text}")
