import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
import sys
import numpy as np

def main():
    df = pd.read_csv('./data.csv')

    # ✅ Ask user for input manually instead of using command-line args
    print("Enter option:")
    print("  s : To display Student details")
    print("  c : To display Course details")
    option = input("Enter your choice (s or c): ").strip()

    if option == 's':
        sid = input("Enter Student ID: ").strip()
        write(process_s_data(df, sid))
        print("Student details processed ✅")

    elif option == 'c':
        cid = input("Enter Course ID: ").strip()
        write(process_c_data(df, cid))
        print("Course details processed ✅")

    else:
        display_error()
        print("Invalid option ❌")

def process_s_data(df, sid):
    courses = df.loc[df['Student id'] == int(sid)]

    if len(courses) == 0:
        display_error()
        sys.exit()

    total = courses[' Marks'].sum()

    student_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Student Data</title>
        <style>
            table {
                border: 1px solid;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Student Details</h1>
        <table>
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
            {% for row in courses %}
            <tr>
                <td>{{ row['Student id'] }}</td>
                <td>{{ row[' Course id'] }}</td>
                <td>{{ row[' Marks'] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2"><b>Total Marks</b></td>
                <td><b>{{ total }}</b></td>
            </tr>
        </table>
    </body>
    </html>
    """
    template = Template(student_template)
    content = template.render(courses=courses.to_dict(orient='records'), total=total)
    return content

def process_c_data(df, cid):
    marks = df.loc[df[' Course id'] == int(cid)]

    if len(marks) == 0:
        display_error()
        sys.exit()

    avg = marks[' Marks'].mean()
    max_marks = marks[' Marks'].max()

    export_plot(marks)

    course_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Course Data</title>
        <style>
            table {
                border: 1px solid;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Course Details</h1>
        <table>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
            <tr>
                <td>{{ avg }}</td>
                <td>{{ max_marks }}</td>
            </tr>
        </table>
        <img src="./bar-chart.png" height="250">
    </body>
    </html>
    """

    template = Template(course_template)
    content = template.render(avg=avg, max_marks=max_marks)
    return content

def display_error():
    error_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Something Went Wrong</title>
    </head>
    <body>
        <h1>Wrong Inputs</h1>
        <p>Something went wrong. Please check your input.</p>
    </body>
    </html>
    """
    template = Template(error_template)
    content = template.render()
    write(content)

def write(content):
    with open("output.html", "w") as f:
        f.write(content)
    print("✅ Output written to file: output.html")

def export_plot(data):
    freq = data[' Marks'].value_counts().sort_index()
    x = np.array(freq.index)

    lower_limit = (x.min() // 10) * 10

    plt.figure(figsize=(10, 6))
    plt.bar(x, freq.values, width=1, align='center')

    plt.xlim(lower_limit, 100)
    plt.xticks(range(lower_limit, 101, 10))

    plt.xlabel('Marks')
    plt.ylabel('Frequency')

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig('bar-chart.png', dpi=300, bbox_inches='tight')
    plt.close()

main()
