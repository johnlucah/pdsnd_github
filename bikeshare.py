import time
import pandas as pd
import numpy as np
import calendar as cal
import tabulate as tab
from IPython.display import display

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DICT = dict([(v.lower(), i) for i, v in enumerate(cal.month_name) if i > 0])

WEEK_DAY_DICT = dict([(v.lower(), i) for i, v in enumerate(cal.day_name)])

def read_option(options, input_message):
    """
    Reads an option that must be defined in the options list (options).

    Returns:
        (list) options - list of available options
        (str) input_message - message showed to user when requesting for input
        (function) parse_func - function used to parse the user input
    """

    selected_option = ''
    while selected_option == '':
        try:
            selected_option = input(input_message).strip().lower()
        except:
            pass

        if selected_option not in options:
            print('Invalid option, try again. \n')
            selected_option = ''

    return selected_option

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    options = CITY_DATA
    input_message = '\nPlease, type the city you would like to analyze ({}): \n'.format(", ".join(map(lambda x: x.title(), options)))
    city = read_option(options, input_message)

    # get user input for month (all, january, february, ... , june)
    options = MONTH_DICT
    options['all'] = -1
    input_message = '\nPlease, type the month you would like to filter ({}): \n'.format(", ".join(map(lambda x: x.title(), options)))
    month = MONTH_DICT[read_option(options, input_message)]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    options = WEEK_DAY_DICT
    options['all'] = -1
    input_message = '\nPlease, type the day of the week ({}): \n'.format(", ".join(map(lambda x: x.title(), options)))
    day = WEEK_DAY_DICT[read_option(options, input_message)]

    print('-'*40)
    return city, month, day

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']

    return df[((month == -1) | (df.month == month)) & ((day == -1) | (df.day == day))]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_index = dict([(v, k.title()) for k, v in MONTH_DICT.items()])
    week_day_index = dict([(v, k.title()) for k, v in WEEK_DAY_DICT.items()])

    # display the most common month
    most_common_month = month_index[df['month'].mode()[0]]
    print('Most common month: {}'.format(most_common_month))

    # display the most common day of week
    most_common_day = week_day_index[df['day'].mode()[0]]
    print('Most common day of week: {}'.format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()
    print('Most commonly used start station: {}'.format(start_station_mode[0]))

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()
    print('Most commonly used end station: {}'.format(end_station_mode[0]))

    # display most frequent combination of start station and end station trip
    most_common_trip = df['trip'].mode()

    print('Most frequent trip (start station -> end station): {}'.format(most_common_trip[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time: {}'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types:')
    user_df = df.groupby('User Type')['User Type'].count()
    print(user_df.head())

    print('\n')

    # Display counts of gender
    if('Gender' in df):
        print("Count of Gender:")
        gender_df = df.groupby('Gender')['Gender'].count()
        print(gender_df.head())
    else:
        print('No Gender data available')

    print('\n')

    # Display year of birth data
    if('Birth Year' in df):
        earliest_year = int(df['Birth Year'].min())
        most_common_year = int(df['Birth Year'].mode()[0])
        most_recent_year = int(df['Birth Year'].max())
        print('Earliest year of birth: {} \nMost recent year of birth: {} \nMost common year of birth: {}'.format(earliest_year, most_recent_year, most_common_year))
    else:
        print('No year of birth data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df) == 0:
            print('\nNo data found with the selected filters, please restart application and try again with different ones !')
            break

        #cleaning data
        if 'Birth Year' in df:
            df['Birth Year'] = pd.to_numeric(df['Birth Year'], downcast = 'integer')

        if 'Gender' in df:
            df['Gender'].fillna(value='Not declared', inplace = True)

        df['User Type'].fillna(value='Unknown', inplace = True)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        page_count = 0
        page_size = 5
        show_data = input('\nWould you like to see the raw data ? Enter yes or no.\n').lower() == 'yes'
        while show_data:
            print(tab.tabulate(df[(page_count * page_size):min((page_count * page_size) + page_size, len(df))]))
            page_count += 1
            if (page_count * page_size) >= len(df):
                print ('Nothing more to display')
                break;

            show_data = input('\nWould you like to see more ? Enter yes or no.\n').lower() == 'yes'

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
