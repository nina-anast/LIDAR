# LIDAR

Κώδικας για το μάθημα Λιμένες και Συνδυασμένες Μεταφορές. Simulation πλοίου το οποίο χρησιμοποιεί Lidar για αποφυγή εμποδίων.

 * Για να αλλάζουμε βασικά μεγέθη του κώδικα πάμε στο ```controllers/wheel_test/demands.py```.

 * Για να ρυθμίζουμε τις συσκευές του ```Robot()``` πηγαίνουμε στο ```controllers/wheel_test/devices.py```.

 * Ο controller που χρησιμοποιούμε τώρα είναι ο ```controllers/wheel_test/wheel_test.py```.

 * Για να τρέξουμε τον κώδικα πηγαίνουμε ```worlds/LiDAR.wbt```.


## Τι υπάρχει εως τώρα:
 
 1. Simulation πλοίου

 2. Controller που διαχειρίζεται έλικα και πηδάλιο
 
 3. Παράλληλα μπορεί να διαβάζεί δεδομένα Lidar Point Cloud αλλά και Rotational Motor για το πηδάλιο


## ToDos: 

 1. Κώδικας για αναγνώριση εμποδίων από το lidar point cloud ```range_image = lidar.getRangeImage()```.

 2. Έλεγχος κινητήρα μέσω του point cloud

 3. Τεχνική Έκθεση

 4. Παρουσίαση?