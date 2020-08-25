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


    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city=input("\nPlease type in the City you'd like to explore. Please select either Chicago, New York City or Washington: ")
            if city.strip().lower() in CITY_DATA:
                print("\nLet's explore the data of {}!".format(city.title().strip()))
                break
            else:
                print('\nThere is no data for this city.')
        except:
            continue


    # get user input for month (all, january, february, ... , june)

    while True:
        try:
            month=input("\nPlease type in a month of which you'd like to explore the data. Please select either months from 'January' to 'June' or 'all' to analyze all months: ")
            if month.strip().lower() in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("\nLet's explore the data of {}!".format(month.title().strip()))
                break
            if month.strip().lower() == 'all':
                print("\nLet's explore the data of all months!")
                break
            if month.strip().lower() in ('july', 'august', 'september', 'october', 'november', 'december'):
                print("\nSorry, the dataset only includes data from January to June.")
            else:
                print('\nUuuups something went wrong. This is not a month.')
        except:
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            day=input("\nPlease type in a day of the week of which you'd like to explore the data. Please select either 'Monday, Tuesday,...' or 'all' to analyze all days of the week: ")
            if day.strip().lower() in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturnday' ,'sunday'):
                print("\nLet's explore the data from {}!".format(day.title().strip()))
                break
            if day.strip().lower() == 'all':
                print("\nLet's explore the data of all days!")
                break
            else:
                print('\nUuuups something went wrong. This is not a day of the week.')
        except:
            continue

    print('-'*40)
    return city.lower(), month, day


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
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.title() != 'All':
        # use the index of the months list to get the corresponding int
       df = df[df['month'] == month.title()]


    # filter by day of week if applicable
    if day.title() != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common **month**
    most_common_month = df['month'].mode()[0]
    print("\nThe most common month is {}.".format(most_common_month))


    # display the most common **day of week**
    most_common_day = df['day'].mode()[0]
    print("\nThe most common day is {}.".format(most_common_day))

    # display the most common **start hour**
    df['hour'] = df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]
    print("\nThe most popular starting hour is {}.".format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most popular start station is {}.".format(popular_start_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe most popular end station is {}.".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['combine_station'] = df['Start Station'] + " AND " + df['End Station']
    most_popular_combination = df['combine_station'].mode()[0]
    print("\nThe most frequent combination of start and end station is {}.".format(most_popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # define 'end time' as timestamp
    df['End Time'] = pd.to_datetime(df['End Time'])

    # calculate travel time in **minutes**
    df['diff_minutes'] = df['End Time'] - df['Start Time']
    df['diff_minutes']=df['diff_minutes']/np.timedelta64(1,'m')

    # calculate travel time in **hours**

    df['diff_hours'] = df['End Time'] - df['Start Time']
    df['diff_hours']=df['diff_hours']/np.timedelta64(1,'h')

    # calculate total travel time (sum) in **minutes** and **hours**

    total_travel_time = df['diff_minutes'].sum().astype(int)
    total_travel_time_hours = df['diff_hours'].sum().astype(int)

    # display total travel time in **minutes** and **hours**

    print("\nThe total travel time is {} MINUTES!".format(total_travel_time))
    print("\nThe total travel time is {} HOURS!".format(total_travel_time_hours))

    # calculate mean travel time in **minutes** and **hours**
    mean_travel_time = df['diff_minutes'].mean()
    mean_travel_time_hours = df['diff_hours'].mean()

    # display mean travel time in **minutes** and **hours**

    print("\nThe average travel time is {:.2f} MINUTES!".format(mean_travel_time))
    print("\nThe average travel time is {:.2f} HOURS!".format(mean_travel_time_hours))


    print('\n'*3)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print("\n This is an overview of the different user types:")
    print(user_types)


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("\n This is an overview of the gender of the bikeshare users:")
        print(gender_count)
    else:
        print("There's no additional data on bikeshare users available for Washington.")


    # Display earliest, most recent, and most common year of birth
    if ('Birth Year') in df.columns:
        earliest_year = df['Birth Year'].min().astype(int)
        recent_year = df['Birth Year'].max().astype(int)
        common_year = df['Birth Year'].mode()[0].astype(int)
        print("\nThe earliest year of birth is {}.".format(earliest_year))
        print("\nThe most recent year of birth is {}.".format(recent_year))
        print("\nThe most common year of birth is {}.".format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """ask user if he would like to see 5 records of raw data. Keep asking until he does not want to see any more data"""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            try:
                raw_data = input('\nWould you like to display 5 records of raw data (yes or no)?').lower().strip()
                if raw_data.strip().lower() == 'yes':
                    i = 0
                    j = 5
                    print(df.iloc[i:j])
                    while True:
                        try:
                            raw_data = input('\nWould you like to display another 5 records of raw data (yes or no)?')
                            if raw_data.strip().lower() == 'yes':
                                i += 5
                                j += 5
                                print(df.iloc[i:j])
                            if raw_data.strip().lower() == 'no':
                                break
                            if raw_data.strip().lower() not in ('yes', 'no'):
                                print("\nUuuup something went wrong choose 'yes' or 'no'")
                        except:
                            continue
                if raw_data.strip().lower() == 'no':
                    break
                if raw_data.strip().lower() not in ('yes', 'no'):
                    print("\nUuuups. Something went wrong. Please select either 'yes' or 'no'")
            except:
                continue


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThanks for taking your time to explore the Bikeshare dataset. Hope to see you soon again!\n')
            break


if __name__ == "__main__":
	main()
