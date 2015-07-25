#!/#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'dommyet'

import os
import shutil
import pickle
import threading
import re
import urllib.request
import urllib.error
import gzip
import time
from collections import deque
import pymysql
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.url_seed = ('genres.php', 'star_list.php?prefix=A',
                         'vl_update.php', 'vl_newentries.php', 'vl_newrelease.php?&mode=2&',
                         'vl_mostwanted.php', 'vl_mostwanted.php?&mode=2&',
                         'vl_bestrated.php', 'vl_bestrated.php?&mode=2&')

        self.url_pool = deque()
        self.url_scanned_pool = deque()
        for i in self.url_seed:
            self.url_pool.append(i)

        # Load previous from files
        try:
            print('[INFO] Restoring scan progress')
            f = open('url_pool.bin', 'rb')
            self.url_pool = pickle.load(f)
            f.close()
            f = open('url_scanned_pool.bin', 'rb')
            self.url_scanned_pool = pickle.load(f)
            f.close()
            print('[INFO] Scan progress restored')
        except FileNotFoundError:
            print('[INFO] File not found')

        # Test database
        try:
            self.mysql()
            self.mysql().close()
        except:
            print('[CRIT] Database error please check settings')
            time.sleep(9999)

        if not os.path.exists('images'):  # Check and create folder
            os.makedirs('images')

        self.re_detail = re.compile(r'\./\?v=\w{10}')
        self.re_genres = re.compile(r'genres\.php')
        self.re_artist = re.compile(r'star_list\.php\?*')
        self.re_update_list = re.compile(r'vl_update\.php\?list*')
        self.re_overview = re.compile(
            r'vl_genre|vl_star|vl_director|vl_maker|vl_label|vl_bestrated|vl_mostwanted|vl_newentries|vl_newrelease|vl_update|star_list|\.php\?*')

        self.flag = True  # Worker control flag

    def get_url(self):
        while len(self.url_pool) > 0:
            url = self.url_pool.popleft()
            if url not in self.url_scanned_pool:
                self.url_scanned_pool.append(url)
                return url
            else:
                time.sleep(5)

    def soup(self, url):
        thread_name = threading.current_thread().getName()
        req = urllib.request.Request('http://www.javlibrary.com/cn/' + url)
        req.add_header('Host', 'www.javlibrary.com')
        req.add_header('Accept', 'text/html, application/xhtml+xml, */*')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
        req.add_header('Referer', 'http://www.javlibrary.com/')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Accept-Language', 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4')

        while True:
            try:  # Open URL
                response = urllib.request.urlopen(req).read()
                try:  # Decompress
                    html = gzip.decompress(response).decode('utf-8', 'ignore')
                except OSError:  # Not compressed
                    html = response.decode('utf-8', 'ignore')
                finally:
                    break  # Jump out from the loop
            except urllib.error.HTTPError as error:  # HTTP error
                print('[WARN] %s # Error %s while opening %s' % (thread_name, error.code, url))
            except urllib.error.URLError:  # URL error
                print('[WARN] %s # URL error while opening %s' % (thread_name, url))
            finally:  # Sleep and retry
                time.sleep(5)
        return BeautifulSoup(html, 'html.parser')

    def mysql(self):
        mysql_host = 'localhost'
        # mysql_sock = 'var/run/mysqld/mysqld.sock'
        mysql_user = 'username'
        mysql_pass = 'password'
        conn = pymysql.connect(
            user=mysql_user, passwd=mysql_pass, host=mysql_host, db='javlibrary', charset='utf8')
        # conn = pymysql.connect(
        #     user=mysql_user, passwd=mysql_pass, host=mysql_host, unix_socket=mysql_sock, db='javlibrary', charset='utf8')
        return conn

    def download(self, url, identity):
        thread_name = threading.current_thread().getName()
        req = urllib.request.Request(url)
        req.add_header('Host', 'pics.dmm.co.jp')
        req.add_header('Accept', 'text/html, application/xhtml+xml, */*')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
        req.add_header('Referer', 'http://www.javlibrary.com/')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Accept-Language', 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4')
        req.add_header('Cache-Control', 'no-cache')

        if not os.path.exists('images' + os.sep + identity):  # Test and create folder
            os.makedirs('images' + os.sep + identity)

        while True:
            try:  # Open URL
                response = urllib.request.urlopen(req)
                output = open('images' + os.sep + identity + os.sep + os.path.split(url)[1], 'wb')
                shutil.copyfileobj(response, output)
                break  # Jump out from the loop
            except urllib.error.HTTPError as error:  # HTTP error
                print('[WARN] %s # Error %s while downloading %s' % (thread_name, error.code, url))
            except urllib.error.URLError:  # URL error
                print('[WARN] %s # URL error while downloading %s' % (thread_name, url))
            except TimeoutError:
                print('[WARN] %s # Timeout error while downloading %s' % (thread_name, url))
            except ConnectionResetError:
                print('[WARN] %s # Connection reset error while downloading %s' % (thread_name, url))
            finally:  # Sleep and retry
                time.sleep(5)

    def dispatch_url(self, url):
        if url not in self.url_scanned_pool:  # URL not scanned
            if self.re_detail.match(url):  # URL matching detail page
                self.url_pool.append(url)
            elif self.re_overview.match(url) and not self.re_update_list.match(url):
                self.url_pool.append(url)  # URL matching overview page, avoid vl_update list view

    def parse_url(self, url, soup):
        if self.re_detail.match(url):  # URL matching detail page
            self.detail_parser(soup)
        elif self.re_genres.match(url):  # URL matching genres page
            self.genres_parser(soup)
        elif self.re_artist.match(url):  # URL matching artist page
            self.artist_parser(soup)
        else:  # URL matching overview page
            self.overview_parser(soup)

    def detail_parser(self, soup):
        video_identity = soup.find('div', id='video_id', class_='item').find('td', class_='text').get_text()

        video_shortlink = soup.find('link', rel='shortlink').get('href')[-10:]

        video_title = soup.title.string.strip(video_identity + ' ').strip(' - JAVLibrary')

        video_date = soup.find('div', id='video_date', class_='item').find('td', class_='text').get_text()

        video_length = soup.find('div', id='video_length', class_='item').find('span', class_='text').get_text()

        try:  # Some video doesn't have score field
            video_score = soup.find('div', id='video_review', class_='item').find('span', class_='score').get_text()
            try:  # Some video doesn't have score
                video_score = str(int(float(video_score.strip('()')) * 100))
            except ValueError:
                video_score = '0'
        except AttributeError:
            video_score = '0'

        video_cover = soup.find('div', id='video_jacket').find('img', id='video_jacket_img').get('src')

        video_preview = []
        try:  # Some video doesn't have preview images
            for i in soup.find('div', class_='previewthumbs').findAll('img'):
                video_preview.append(i.get('src'))
        except AttributeError:
            pass

        conn = self.mysql()
        cursor = conn.cursor()

        # Table videos
        cursor.execute('SELECT vlink FROM videos WHERE vlink = %s', video_shortlink)
        if not cursor.fetchall():  # If entry not exist insert entry
            item = [video_identity, video_shortlink, video_title, video_date, video_length, video_score, video_cover]
            while True:
                try:
                    cursor.execute('INSERT INTO videos (id, vlink, title, date, length, score, cover) VALUES (%s, %s, %s, %s, %s, %s, %s)', item)
                    break
                except pymysql.err.InternalError:  # Suppress lock wait timeout exceeded error
                    time.sleep(1)
        else:  # If entry exist update entry
            item = [video_date, video_length, video_score, video_cover, video_shortlink]
            cursor.execute('UPDATE videos SET date = %s, length = %s, score = %s, cover = %s WHERE vlink = %s', item)

        # Table previews
        for i in video_preview:
            cursor.execute('SELECT vlink FROM previews WHERE vlink = %s AND url = %s', (video_shortlink, i))
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO previews (vlink, url) VALUES (%s, %s)', (video_shortlink, i))

        # Table list_directors, directors
        for i in soup.find('div', id='video_director').findAll('a', rel='tag'):
            video_director = [i.get('href')[18:], i.get_text()]
            if video_director[1] != '----':  # Some video doesn't have director
                cursor.execute('SELECT dlink FROM list_directors WHERE dlink = %s', video_director[0])
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO list_directors (dlink, name) VALUES (%s, %s)', video_director)
                cursor.execute('SELECT dlink FROM directors WHERE dlink = %s AND vlink = %s', (video_director[0], video_shortlink))
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO directors (dlink, vlink) VALUES (%s, %s)', (video_director[0], video_shortlink))

        # Table list_makers, makers
        for i in soup.find('div', id='video_maker').findAll('a', rel='tag'):
            video_maker = [i.get('href')[15:], i.get_text()]
            if video_maker[1] != '----':  # Some video doesn't have maker
                cursor.execute('SELECT mlink FROM list_makers WHERE mlink = %s', video_maker[0])
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO list_makers (mlink, name) VALUES (%s, %s)', video_maker)
                cursor.execute('SELECT mlink FROM makers WHERE mlink = %s AND vlink = %s', (video_maker[0], video_shortlink))
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO makers (mlink, vlink) VALUES (%s, %s)', (video_maker[0], video_shortlink))

        # Table list_issuers, issuers
        for i in soup.find('div', id='video_label').findAll('a', rel='tag'):
            video_issuer = [i.get('href')[15:], i.get_text()]
            if video_issuer[1] != '----':  # Some video doesn't have issuer
                cursor.execute('SELECT ilink FROM list_issuers WHERE ilink = %s', video_issuer[0])
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO list_issuers (ilink, name) VALUES (%s, %s)', video_issuer)
                cursor.execute('SELECT ilink FROM issuers WHERE ilink = %s AND vlink = %s', (video_issuer[0], video_shortlink))
                if not cursor.fetchall():  # If entry not exist insert entry
                    cursor.execute('INSERT INTO issuers (ilink, vlink) VALUES (%s, %s)', (video_issuer[0], video_shortlink))

        # Table list_genres, genres
        for i in soup.find('div', id='video_genres').findAll('a', rel='category tag'):
            video_genres = [i.get('href')[15:], i.get_text()]
            cursor.execute('SELECT glink FROM list_genres WHERE glink = %s AND name = %s', video_genres)
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO list_genres (glink, name) VALUES (%s, %s)', video_genres)
            cursor.execute('SELECT glink FROM genres WHERE glink = %s AND vlink = %s', (video_genres[0], video_shortlink))
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO genres (glink, vlink) VALUES (%s, %s)', (video_genres[0], video_shortlink))

        # Table list_artists, artists
        for i in soup.find('div', id='video_cast').findAll('a', rel='tag'):
            video_artist = [i.get('href')[14:], i.get_text()]
            cursor.execute('SELECT alink FROM list_artists WHERE alink = %s', video_artist[0])
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO list_artists (alink, name) VALUES (%s, %s)', video_artist)
            cursor.execute('SELECT alink FROM artists WHERE alink = %s AND vlink = %s', (video_artist[0], video_shortlink))
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO artists (alink, vlink) VALUES (%s, %s)', (video_artist[0], video_shortlink))

        conn.commit()  # Commit together
        cursor.close()
        conn.close()

        # Download images
        self.download(video_cover, video_identity)  # Download cover
        for i in video_preview:
            self.download(i, video_identity)  # Download previews

    def genres_parser(self, soup):
        conn = self.mysql()
        cursor = conn.cursor()
        for a in soup.findAll('div', class_='genreitem'):  # Assemble item
            item = []
            item.append(a.find('a', href=True).get('href')[15:])  # Genres shortlink
            item.append(a.find('a', href=True).get_text())  # Genres name
            cursor.execute('SELECT glink, name FROM list_genres WHERE glink = %s and name = %s', item)
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO list_genres (glink, name) VALUES (%s, %s)', item)
        conn.commit()  # Commit together
        cursor.close()
        conn.close()

    def artist_parser(self, soup):
        conn = self.mysql()
        cursor = conn.cursor()
        for a in soup.find('div', class_='starbox').findAll('div', class_='searchitem'):  # Assemble item
            item = []
            item.append(a.get('id'))  # Artist shortlink
            item.append(a.find('a').get_text())  # Artist name
            cursor.execute('SELECT alink FROM list_artists WHERE alink = %s', item[0])
            if not cursor.fetchall():  # If entry not exist insert entry
                cursor.execute('INSERT INTO list_artists (alink, name) VALUES (%s, %s)', item)
        conn.commit()  # Commit together
        cursor.close()
        conn.close()
        pass

    def overview_parser(self, soup):
        conn = self.mysql()
        cursor = conn.cursor()

        if not soup.find('em'):  # Check empty page
            for a in soup.find('div', class_='videos').findAll('div', class_='video', id=True):
                video_identity = a.find('div', class_='id').get_text()
                video_shortlink = a.find('a', class_='icn_want', id=True).get('id')
                video_title = a.find('div', class_='title').get_text().encode('gbk', 'ignore').decode('gbk')
                video_thumbnail = a.find('img', src=True).get('src')
                cursor.execute('SELECT vlink FROM videos WHERE vlink = %s', video_shortlink)
                if not cursor.fetchall():  # If entry not exist insert entry
                    item = [video_identity, video_shortlink, video_title, video_thumbnail]
                    while True:
                        try:
                            cursor.execute('INSERT INTO videos (id, vlink, title, thumbnail) VALUES (%s, %s, %s, %s)', item)
                            break
                        except pymysql.err.InternalError:  # Avoid 'Lock wait timeout exceeded'?
                            time.sleep(1)
                        except pymysql.err.IntegrityError: # Avoid 'Duplicated entry'?
                            break

                else:  # If entry exist update entry
                    item = [video_title, video_thumbnail]
                    while True:
                        try:
                            cursor.execute('UPDATE videos SET title = %s, thumbnail = %s', item)
                            break
                        except pymysql.err.InternalError:
                            time.sleep(1)  # Avoid strange deadlock found when trying to get lock?

                # Download images
                if video_thumbnail != '../img/noimageps.gif':  # Avoid no thumbnail error
                    self.download(video_thumbnail, video_identity)  # Download thumbnail

            conn.commit()  # Commit together
            cursor.close()
            conn.close()

    def worker(self):
        thread_name = threading.current_thread().name
        print('[INFO] %s # Started' % thread_name)

        while self.flag:  # Worker control flag True
            url = self.get_url()
            if url:
                time_start = time.time()
                print('[INFO] %s # Parsing %s' % (thread_name, url))

                # Read contents
                soup = self.soup(url)

                # Extract and parse all URLs
                for i in soup.findAll('a', href=True):
                    self.dispatch_url(i.get('href'))

                # Parse myself
                self.parse_url(url, soup)

                time_end = time.time()
                print('[INFO] %s # Job finished in %0.1f seconds' % (thread_name, time_end - time_start))

        # Control flag False terminate self
        print('[INFO] %s # Terminated' % thread_name)

    def main(self, threads):
        time.sleep(5)
        for i in range(threads):
            t = threading.Thread(target=self.worker)
            t.start()
        time.sleep(5)

        while len(self.url_pool) > 0:
            print('[INFO] %s URLs in pool, %s URLs scanned' % (len(self.url_pool), len(self.url_scanned_pool)))

            try:
                f = open('url_pool.bin', 'wb')
                pickle.dump(self.url_pool, f)
                f.close()
                f = open('url_scanned_pool.bin', 'wb')
                pickle.dump(self.url_pool, f)
                f.close()
                # print('[INFO] Scan progress saved')
            except:
                print('[WARN] Save scan progress failed')

            time.sleep(60)

        self.flag = False  # Set termination flag
        t.join()

if __name__ == '__main__':
    Spider().main(8)
