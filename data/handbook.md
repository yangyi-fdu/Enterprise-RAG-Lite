# Halden Robotics Employee Handbook

Halden Robotics is a fictional company that builds autonomous mobile robots for warehouse logistics. This handbook is sample data for the retrieval demo. All names, numbers and policies in it are invented.

## 1. Company overview

Halden Robotics was founded in 2019 and has its headquarters in Busan, with a second engineering office in Daejeon. The company has around 240 employees. The Chief Executive Officer is Mina Kwon and the Chief Technology Officer is Daniel Reyes. Halden's main product is the HR-7 autonomous mobile robot, which carries loads of up to 300 kilograms and navigates using lidar and a fused wheel odometry and IMU estimate. A smaller model, the HR-3, carries up to 60 kilograms and is designed for retail stockrooms.

## 2. Working hours and remote work

Core working hours are 10:00 to 16:00 Korea Standard Time. Outside core hours, employees may arrange their schedule with their manager. Employees may work remotely for up to two days per week after completing their probation period. Remote work requests are submitted through the HR portal at least one working day in advance. Hardware engineers who need lab access should coordinate remote days with the lab manager. The probation period for new employees lasts three months.

## 3. Leave policy

Full-time employees receive 15 days of paid annual leave per year, increasing by one day for every two years of service up to a maximum of 25 days. Unused annual leave can be carried over into the next year up to a limit of 5 days; any remaining days expire on 31 March. Sick leave of up to 3 consecutive days does not require a medical certificate; longer absences require a certificate from a doctor. Employees also receive 2 paid volunteering days per year. Leave requests must be approved by the direct manager in the HR portal.

## 4. Expenses and reimbursement

Business expenses must be submitted through the Expensify system within 30 days of the purchase date. Every claim must include an itemised receipt; a card statement alone is not accepted. Meals during business travel are reimbursed up to 40,000 won per day. Claims under 500,000 won are approved by the direct manager. Claims of 500,000 won or more also require approval from the finance controller, Jae-won Park. Approved claims are paid with the next monthly salary, which is paid on the 25th of each month. Alcohol is not reimbursable unless it is part of an approved client event.

## 5. Business travel

All business travel must be booked through the travel desk at least 14 days before departure, except in emergencies approved by a department head. Economy class is the standard for flights under 6 hours; premium economy may be booked for flights of 6 hours or longer. Hotel costs are reimbursed up to 180,000 won per night in Seoul and 130,000 won per night in other Korean cities. For international trips, employees must register their itinerary with the travel desk so that the company can contact them in an emergency. Travel insurance is provided automatically for all booked trips.

## 6. IT support and equipment

Each new employee receives a laptop on their first day. Software engineers receive a workstation with an NVIDIA RTX 4090 GPU on request. To report a hardware fault or request software, open a ticket in the IT service desk at help.halden.example. Urgent problems that block work can be reported by phone on extension 4400. Employees must not open laptops or workstations themselves to repair them, because this voids the warranty. Lost or stolen devices must be reported to IT within 24 hours.

## 7. Information security

All company accounts use single sign-on with mandatory two-factor authentication. Passwords must be at least 14 characters long and must not be reused from other services. Source code may only be stored in the company GitLab instance; uploading company code to public repositories or personal cloud storage is prohibited. The guest Wi-Fi network is isolated from the internal network and must never be used to transfer customer data or robot map files. Suspected phishing emails should be forwarded to the security team at security@halden.example. Security awareness training is mandatory and must be completed every 12 months.

## 8. Robot lab safety

Access to the robot test arena requires completion of the lab safety induction, which takes about 2 hours and is run every Tuesday. Safety shoes must be worn in the arena at all times. During autonomous runs, a second person must stand at the emergency stop and be ready to press it. The speed limit for robots in the shared test arena is 1.2 metres per second; tests above this speed must be booked in the closed high-speed bay. Lithium battery packs must be charged only in the fire-rated charging cabinets and never left charging overnight. Any collision, near miss or injury must be reported in the incident log on the same day.

## 9. Software development process

Engineering teams work in two-week sprints. Every change to the robot software must go through a merge request with at least one approving review before it is merged into the main branch. The robot software stack is built on ROS 2 Humble and runs on Ubuntu 22.04. Continuous integration runs unit tests and a simulation regression suite in Gazebo for every merge request; a merge request cannot be merged if the simulation suite fails. Releases to customer robots happen once a month, after a 48-hour soak test on the HR-7 fleet in the test arena.

## 10. Learning and development

Each employee has an annual learning budget of 1,500,000 won, which can be spent on courses, books and conference tickets. Conference travel is paid from the travel budget, not the learning budget. Employees who want to attend an international conference should submit a request to their manager at least 6 weeks in advance. Internal tech talks take place every second Thursday at 17:00.

## 11. Onboarding

On the first day, new employees meet their onboarding buddy, collect their laptop and badge, and complete the IT security setup. During the first week they complete the lab safety induction and the information security training. Each new employee has a 30-60-90 day plan agreed with their manager. Questions about payroll should be directed to the people team at people@halden.example.
