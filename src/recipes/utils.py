import matplotlib.pyplot as plt 
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG') # For writing to file-like object
    plt.figure(figsize=(6, 3))

    if chart_type == '#1':
        # Bar chart of food types vs number of matching recipes
        data['food_type'].value_counts().plot(kind='bar')
        plt.title('Recipe Count by Food Type')
        plt.xlabel('Food Type')
        plt.ylabel('Count')

    elif chart_type == '#2':
        # Pie chart of difficulties
        data['difficulty'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Difficulty Distribution')
        plt.ylabel('')

    elif chart_type == '#3':
        # Line chart of cooking_times (sorted)
        data = data.sort_values(by='cooking_time')
        plt.plot(data['name'], data['cooking_time'], marker='o')
        plt.xticks(rotation=45, ha='right')
        plt.title('Cooking Time by Recipe')
        plt.xlabel('Recipe')
        plt.ylabel('Time (min)')

    else:
        plt.text(0.5, 0.5, 'Invalid Chart Type', ha='center')

    plt.tight_layout()
    return get_graph()