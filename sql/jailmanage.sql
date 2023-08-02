-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 02, 2023 at 10:12 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jailmanage`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`name`, `email`, `password`) VALUES
('Chowdhury Zaber Bin Zahid', 'czaber49@gmail.com', '93a5086d4a0f21b634c2518c249523247ebba14f0cabf5ae5bee54bfd5588556');

-- --------------------------------------------------------

--
-- Table structure for table `prisoner`
--

CREATE TABLE `prisoner` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `age` int(11) NOT NULL,
  `birth` date NOT NULL,
  `record` varchar(50) NOT NULL,
  `cell` varchar(50) NOT NULL,
  `year` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `prisoner`
--

INSERT INTO `prisoner` (`id`, `name`, `age`, `birth`, `record`, `cell`, `year`) VALUES
(1, 'Apu Kumar Roy', 25, '2013-07-10', 'Human Trafficking', '1A', '10 years'),
(8, 'Kala Manik', 45, '1993-07-12', 'Drug Dealing', '2A', '5 years'),
(12, 'Alison Burger', 45, '1995-07-11', 'Robbery', '1B', '2 years'),
(14, 'Ted Bundy', 40, '1970-07-05', 'Serial Killer', '2B', 'Death Sentence');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `email` varchar(200) NOT NULL,
  `shift` varchar(200) NOT NULL,
  `reason` varchar(1000) NOT NULL,
  `role` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

CREATE TABLE `schedule` (
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `type` varchar(200) NOT NULL,
  `shift` varchar(200) NOT NULL,
  `time` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `schedule`
--

INSERT INTO `schedule` (`name`, `email`, `type`, `shift`, `time`) VALUES
('Bilkis Begum', 'bilkis@gmail.com', 'Wash Dish', 'Day', '8AM - 3PM'),
('Kuddus Miah', 'kuddus@gmail.com', 'Laundry', 'Night', '9PM - 12AM'),
('Safwat Samir', 'samir@gmail.com', 'Guard Room 1', 'Day', '8AM - 3PM'),
('Walid Ibne Hasan', 'walid@gmail.com', 'Room Cleaning', 'Night', '9PM - 12AM');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `role` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `role`, `email`, `password`) VALUES
(1, 'Kuddus Miah', 'Police', 'kuddus@gmail.com', '75f7f8c26cfe31a47113a7ce0b3493277cf392879e6fca1ebc7d93e597914e0c'),
(5, 'Bilkis Begum', 'Chef', 'bilkis@gmail.com', 'bd514b20441bbbfe4edc22079e690736dcc888de2496c55963f9f5e2b43530f3'),
(9, 'Walid Ibne Hassan', 'Cleaner', 'walid@gmail.com', '4ad57ab610196a7c72e8e06824674470d16e10932ce9d5214cebcc4fdf3e3218'),
(12, 'Shuvo Ahmed', 'Cleaner', 'shuvo@gmail.com', '2f684da2a727e1c49e48764b0c284c4835123ab7a330758066ed9b2b8721b810'),
(14, 'Safwat Samir', 'Police', 'samir@gmail.com', 'b816a16cd03774e0cefac03765680a33365d0b16060f67a2f7382a844f9c664f'),
(15, 'Abu Fatah Mohammad Faisal', 'Cleaner', 'faisal@gmail.com', 'b0d964d1ed25d44c646fe86afcec8a56304bb4be36c01ea4d14785e4a6dc2ba7');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `prisoner`
--
ALTER TABLE `prisoner`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `request`
--
ALTER TABLE `request`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `prisoner`
--
ALTER TABLE `prisoner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
