import re
import pandas as pd

def preprocess(data):
    # Define the pattern to match the date and time in the chat log
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Split the chat data into messages using the date-time pattern
    messages = re.split(pattern, data)[1:]
    
    # Extract the date-time strings
    dates = re.findall(pattern, data)
    
    # Create a DataFrame with the messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Convert 'message_date' to datetime type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce', dayfirst=True)

    # Drop rows with invalid dates (NaT)
    df.dropna(subset=['message_date'], inplace=True)
    
    # Rename 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Split user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # User name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    
    # Drop the 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract additional date and time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Create a period column to represent hour ranges
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f'{hour}-00')
        elif hour == 0:
            period.append(f'00-1')
        else:
            period.append(f'{hour}-{hour + 1}')
    df['period'] = period

    return df

# Example usage
if __name__ == "__main__":
    with open('your_data_file.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    
    df = preprocess(data)
    print(df.head())
