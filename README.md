# game space invaiders

Space Invaders adalah game sederhana yang, di mana pemain mengendalikan pesawat untuk menembak pesawat alien yang bergerak di layar. Pemain dapat menggerakkan pesawat ke kiri dan kanan, serta menembak peluru untuk menghancurkan pesawat alien . Game ini melibatkan elemen seperti pergerakan objek, deteksi tabrakan, animasi, dan sistem skor, .

dengan menerapkan konsep OOP:
* **Encapsulation** berarti menyembunyikan detail implementasi internal dari sebuah objek dengan menggunakan atribut dan metode yang diatur aksesnya. Berikut penerapannya dalam kode:
  * Atribut dan metode privat menggunakan underscore (_) di awal nama seperti self._x, self._y, self._bullets, dan self._speed.
  * Hal ini membatasi akses langsung ke atribut tersebut dari luar kelas, sehingga mempromosikan data hiding.

* **Inheritance** (pewarisan) memungkinkan kelas untuk mewarisi atribut dan metode dari kelas lain.
  * GameObject adalah kelas dasar (abstrak) yang menjadi parent untuk Player, Enemy, dan FinalBoss.
  * FinalBoss mewarisi dari Enemy, memperluas fungsionalitasnya dengan atribut tambahan seperti _health dan perilaku unik untuk gerakan dan penembakan.

* **Polymorphism** memungkinkan metode yang sama untuk memiliki perilaku yang berbeda tergantung pada kelas turunan yang mengimplementasikannya.
   * Metode draw: Semua kelas (Player, Enemy, FinalBoss) memiliki metode draw, tetapi implementasinya berbeda sesuai dengan kebutuhan masing-masing kelas.
      FinalBoss menambahkan health bar saat menggambar objek,
      Enemy hanya menggambar musuh tanpa health bar
   * Metode move: Kelas turunan (Enemy dan FinalBoss) mengimplementasikan logika gerakan yang berbeda:
      Enemy bergerak lurus ke bawah,
      FinalBoss bergerak secara horizontal dan vertikal dengan bouncing di tepi layar.

* **Abstraction** adalah penyembunyian detail implementasi dan hanya menyediakan antarmuka yang diperlukan.
   * Penggunaan ABC dan metode abstrak (@abstractmethod) dalam GameObject:
      Kelas ini mendefinisikan kerangka dasar untuk semua objek dalam game (seperti draw dan move) tanpa menyediakan implementasi spesifik,
      Kelas turunan (Player, Enemy, dan FinalBoss) harus mengimplementasikan metode ini.

