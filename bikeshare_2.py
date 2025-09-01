import time
import pandas as pd
import numpy as np

# Mapping of available datasets
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.
    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikeshare data.\n")

    # CITY
    while True:
        city = input("Choose a city (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please try again.")

    # MONTH
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (january - june) or 'all': ").lower()
        if month in months:
            break
        else:
            print("Invalid month. Please try again.")

    # DAY
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Choose a day of the week or 'all': ").lower()
        if day in days:
            break
        else:
            print("Invalid day. Please try again.")

    print(f"\nFilters applied: City = {city.title()}, Month = {month.title()}, Day = {day.title()}")
    print('-' * 50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['month'] = df['Start Time'].dt.month_name().str.lower()

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # Most common month
    popular_month = df['month'].mode()
    print("Most common month:", popular_month.iloc[0] if not popular_month.empty else "No data")

    # Most common day of week
    popular_day = df['day_of_week'].mode()
    print("Most common day of week:", popular_day.iloc[0] if not popular_day.empty else "No data")

    # Most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()
    print("Most common start hour:", popular_hour.iloc[0] if not popular_hour.empty else "No data")

    print(f"\nTime to calculate: {time.time() - start_time:.2f} seconds")
    print('-' * 50)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # Most commonly used start station
    popular_start = df['Start Station'].mode()
    print("Most popular start station:", popular_start.iloc[0] if not popular_start.empty else "No data")

    # Most commonly used end station
    popular_end = df['End Station'].mode()
    print("Most popular end station:", popular_end.iloc[0] if not popular_end.empty else "No data")

    # Most frequent combination of start and end station
    if not df.empty:
        common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print("Most frequent combination of start and end station:", common_trip)
    else:
        print("No trip data available.")

    print(f"\nTime to calculate: {time.time() - start_time:.2f} seconds")
    print('-' * 50)


def trip_duration_stats(df):
    """Displays statistics on total and average trip duration."""
    print('\nCalculating Trip Duration...')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()

    print(f"Total travel time: {total_duration:.2f} seconds")
    print(f"Mean travel time: {mean_duration:.2f} seconds")

    print(f"\nTime to calculate: {time.time() - start_time:.2f} seconds")
    print('-' * 50)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...')
    start_time = time.time()

    # User types
    if 'User Type' in df.columns:
        print("\nCounts of user types:\n", df['User Type'].value_counts())
    else:
        print("\nNo user type data available.")

    # Gender
    if 'Gender' in df.columns:
        print("\nCounts of gender:\n", df['Gender'].value_counts())
    else:
        print("\nNo gender data available.")

    # Birth year stats
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode().iloc[0])
        print(f"\nEarliest birth year: {earliest}")
        print(f"Most recent birth year: {latest}")
        print(f"Most common birth year: {common}")
    else:
        print("\nNo birth year data available.")

    print(f"\nTime to calculate: {time.time() - start_time:.2f} seconds")
    print('-' * 50)

def display_raw_data(df):
    """
    Prompt the user if they want to see raw data.
    Display 5 rows at a time until the user says 'no' or data ends.
    """
    row_start = 0
    row_end = 5

    while True:
        show_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").lower()
        if show_data != 'yes':
            break
        print(df.iloc[row_start:row_end])
        row_start += 5
        row_end += 5
        if row_start >= len(df):
            print("\nEnd of data reached.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data available for the selected filters.\n")
        else:
            display_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart != 'yes':
            break
    
    


if __name__ == "__main__":
    main()
