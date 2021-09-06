from hhbot.driver import HeadHunterBot
from time import sleep
import pandas as pd
import datetime 
from settings.settings import EMAIL, HH_PASSWORD, HH_RESUME, email_settings


def parse_views_time():
    with HeadHunterBot(EMAIL, HH_PASSWORD, HH_RESUME, email_settings, invisible=False) as bot:
        bot.start()
        print("logined quite")
        bot.click_on('my_resume')
        bot.click_on('history_btn')
        sleep(10)
        resume_views = bot.find_elements("//span[@class = 'resume-view-history-views']")
        views_time = []
        for resume_view in resume_views:
            views_time.append(resume_view.text)

        try:
            expandable_btn = bot.find_elements("//span[contains(@class,'bloko-link-switch')]")
            for btn in expandable_btn:
                sleep(7)
                btn.click()
            expandable_views = bot.find_elements("//span[@class='g-expandable']")
            for view in expandable_views:
                view = view.text.split(', ')
                views_time.extend(view)
        except Exception as e:
            print('no expandable elements')

        return views_time


def rolling_4hour_forward_count(df):
    df['counter'] = 0
    timedeltas = df['times'] - df['times']
    for index, row in df.iterrows():
        for i in range(index+1, df.shape[0]):
            timedeltas.iloc[i] = df.iloc[i].times - row.times
        tmp = df.iloc[index:]
        df['counter'].iloc[index] = tmp[timedeltas.iloc[index:] <= pd.Timedelta(hours=4)].shape[0]

    return df

def get_update_points(df):
    tmp = df[:]
    tops = []
    for i in range(2):
        try:
            top_time = tmp[tmp.counter == tmp.counter.max()].times.iloc[0]
            tmp = tmp[tmp.times - top_time > pd.Timedelta(hours=4)]
            tops.append(str(top_time.time()))
        except Exception as e:
            print(str(e))
    
    if len(tops) < 2:
        tops = ['9:30:00', '15:30:00']
    return tops


if __name__ == '__main__':
    views_time = parse_views_time()
    df = pd.DataFrame(views_time, columns=['times'])
    df.times = df.times.map(datetime.time.fromisoformat)
    df['times'] = df.times.apply(lambda x: datetime.datetime(year=2000, month=1, day=1, hour=x.hour, minute=x.minute)) 
    df = df.sort_values(by='times').reset_index(drop=True)
    df = rolling_4hour_forward_count(df)
    res = get_update_points(df)
    print(res)