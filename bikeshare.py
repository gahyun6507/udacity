import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ""
    month = ""
    day = ""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in CITY_DATA:
        city = input('Enter a city (Chicago, New York City, Washington): ')
        if city.lower() not in CITY_DATA:
            print('Invalid city. Please enter a valid city.')

    # get user input for month (all, january, february, ... , june)
    while month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Enter a month (all, January, February, March, April, May, June): ')
        if month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print('Invalid month. Please enter a valid month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Enter a day of the week (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ')
        if day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('Invalid day. Please enter a valid day.')



    print('-'*40)
    return city.lower(), month.lower(), day.lower()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data for the specified city
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = MONTHS.index(month.lower()) + 1
        df = df[df['Month'] == month_num]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month_num = df['Month'].mode()[0]
    most_common_month_name = MONTHS[most_common_month_num - 1].capitalize()
    print(f"Most Popular Month: {most_common_month_name}")

    # display the most common day of week
    most_common_week = df['Day of Week'].mode()[0]
    print(f"Most Popular Day of Week: {most_common_week}")

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print(f"Most Popular Start Hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most Popular Start Station: {most_common_start_station}")


    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most Popular End Station: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Frequent Combination of Start Station and End Station Trip: {most_frequent_combination}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of User Types: {user_types}")

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        print(gender_counts)
    else:
        print("\nGender information not available for this dataset.")




    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print("\nBirth Year Statistics:")
        print(f"Earliest Birth Year: {earliest_birth_year}")
        print(f"Most Recent Birth Year: {most_recent_birth_year}")
        print(f"Most Common Birth Year: {most_common_birth_year}")
    else:
        print("\nBirth year information not available for this dataset.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def display_raw_data(df):

    start_idx = 0
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break

        print(df.iloc[start_idx : start_idx + 5])

        start_idx += 5


if __name__ == "__main__":
	main()
