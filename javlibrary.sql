-- phpMyAdmin SQL Dump
-- version 4.2.12deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 08, 2015 at 11:05 PM
-- Server version: 5.5.44-0+deb8u1
-- PHP Version: 5.6.9-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `javlibrary`
--

-- --------------------------------------------------------

--
-- Table structure for table `artists`
--

CREATE TABLE IF NOT EXISTS `artists` (
  `alink` char(6) NOT NULL COMMENT 'Primary Key: Artist shortlink.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `directors`
--

CREATE TABLE IF NOT EXISTS `directors` (
  `dlink` char(4) NOT NULL COMMENT 'Primary Key: Director shortlink.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `genres`
--

CREATE TABLE IF NOT EXISTS `genres` (
  `glink` char(4) NOT NULL COMMENT 'Primary Key: Genres shortlink.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `issuers`
--

CREATE TABLE IF NOT EXISTS `issuers` (
  `ilink` char(4) NOT NULL COMMENT 'Primary Key: Issuer shortlink.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `list_artists`
--

CREATE TABLE IF NOT EXISTS `list_artists` (
  `alink` char(6) NOT NULL COMMENT 'Primary key: Unique artist shortlink.',
  `name` varchar(32) NOT NULL COMMENT 'Artist name.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `list_directors`
--

CREATE TABLE IF NOT EXISTS `list_directors` (
  `dlink` char(4) NOT NULL COMMENT 'Primary key: Unique director shortlink.',
  `name` varchar(32) NOT NULL COMMENT 'Director name.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `list_genres`
--

CREATE TABLE IF NOT EXISTS `list_genres` (
  `glink` char(4) NOT NULL COMMENT 'Primary key: Unique genres shortlink.',
  `name` varchar(16) NOT NULL COMMENT 'Primary key: Genres name.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `list_issuers`
--

CREATE TABLE IF NOT EXISTS `list_issuers` (
  `ilink` char(4) NOT NULL COMMENT 'Primary key: Unique issuer shortlink.',
  `name` varchar(32) NOT NULL COMMENT 'Issuer name.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `list_makers`
--

CREATE TABLE IF NOT EXISTS `list_makers` (
  `mlink` char(4) NOT NULL COMMENT 'Primary key: Unique maker shortlink.',
  `name` varchar(32) NOT NULL COMMENT 'Maker name.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `makers`
--

CREATE TABLE IF NOT EXISTS `makers` (
  `mlink` char(4) NOT NULL COMMENT 'Primary Key: Maker shortlink.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `previews`
--

CREATE TABLE IF NOT EXISTS `previews` (
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.',
  `url` varchar(128) NOT NULL COMMENT 'Primary Key: Image URL.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `videos`
--

CREATE TABLE IF NOT EXISTS `videos` (
  `id` varchar(16) NOT NULL COMMENT 'Primary Key: Video identifier.',
  `vlink` char(10) NOT NULL COMMENT 'Primary Key: Video shortlink.',
  `title` varchar(192) NOT NULL COMMENT 'Primary Key: Video title.',
  `date` date DEFAULT NULL COMMENT 'Release date.',
  `length` int(3) DEFAULT NULL COMMENT 'Video length.',
  `score` int(3) DEFAULT NULL COMMENT 'User rating.',
  `thumbnail` varchar(128) DEFAULT NULL COMMENT 'Thumbnail image URL.',
  `cover` varchar(128) DEFAULT NULL COMMENT 'Cover image URL.',
  `media` varchar(64) DEFAULT NULL COMMENT 'Media file URL.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artists`
--
ALTER TABLE `artists`
 ADD PRIMARY KEY (`alink`,`vlink`);

--
-- Indexes for table `directors`
--
ALTER TABLE `directors`
 ADD PRIMARY KEY (`dlink`,`vlink`);

--
-- Indexes for table `genres`
--
ALTER TABLE `genres`
 ADD PRIMARY KEY (`glink`,`vlink`);

--
-- Indexes for table `issuers`
--
ALTER TABLE `issuers`
 ADD PRIMARY KEY (`ilink`,`vlink`);

--
-- Indexes for table `list_artists`
--
ALTER TABLE `list_artists`
 ADD PRIMARY KEY (`alink`);

--
-- Indexes for table `list_directors`
--
ALTER TABLE `list_directors`
 ADD PRIMARY KEY (`dlink`);

--
-- Indexes for table `list_genres`
--
ALTER TABLE `list_genres`
 ADD PRIMARY KEY (`glink`,`name`);

--
-- Indexes for table `list_issuers`
--
ALTER TABLE `list_issuers`
 ADD PRIMARY KEY (`ilink`);

--
-- Indexes for table `list_makers`
--
ALTER TABLE `list_makers`
 ADD PRIMARY KEY (`mlink`);

--
-- Indexes for table `makers`
--
ALTER TABLE `makers`
 ADD PRIMARY KEY (`mlink`,`vlink`);

--
-- Indexes for table `previews`
--
ALTER TABLE `previews`
 ADD PRIMARY KEY (`vlink`,`url`);

--
-- Indexes for table `videos`
--
ALTER TABLE `videos`
 ADD PRIMARY KEY (`id`,`vlink`,`title`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
