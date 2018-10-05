import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']

WEEKDAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please input the city name('chicago', 'new york city', or 'washington') to analyze:").lower()
    while city not in CITY_DATA:
        city = input("Please input the city name('chicago', 'new york city', or 'washington') to analyze:").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please input the month(all, january, february, march, ...) you want to filter by:").lower()
    while (month != 'all') and (month not in MONTHS):
        month = input("Please input the month you want to filter by:").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please input the week day(all, monday, tuesday, ...) you want to filter by:").lower()
    while (day != 'all') and (day not in WEEKDAYS):
        day = input("Please input the week day you want to filter by:").lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is {}.".format(MONTHS[popular_month-1]))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day is {}.".format(popular_day))

    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour is {}.".format(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}.".format(popular_start_station)) 

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}.".format(popular_end_station)) 

    # display most frequent combination of start station and end station trip
    popular_trip = (df['Start Station'] + ' -> ' + df['End Station']).mode()[0]    
    print("The most frequent trip is {}.".format(popular_trip)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is {:,} seconds.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is {:.2f} seconds.".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types is {}.".format(len(df['User Type'].value_counts())))

    # Display counts of gender
    if 'Gender' in df:
        print("Counts of gender is {}.".format(len(df['Gender'].value_counts())))
    else:
        print("No gender column in the data!")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("The earliest year of birth is {}.".format(int(df['Birth Year'].sort_values().iloc[0])))
        print("The most recent year of birth is {}.".format(int(df['Birth Year'].sort_values(ascending=False).iloc[0])))
        print("The most common year of birth is {}.".format(int(df['Birth Year'].mode()[0])))
    else:
        print("No birth year column in the data!")

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
