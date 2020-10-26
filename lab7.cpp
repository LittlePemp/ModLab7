#include <stdio.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstring>
#include <string>


using namespace std;



struct booker
{
/*Структура данных о книге включает:
	ID книги - code
	Автора книги - author
	Название книги title
	Год написания/публикации year
	Расположение(номер стелажа) place*/
	
	int code;
	char author[30];
	char title[50];
	int year;
	int place;
};



void sort_by_author(booker a[], int n)
/*Сортирока пузырьком по атрибуту author*/
{

	booker min;
	int n_min;

	for (int i = 0; i < n; i++) 
	{
		min = a[i]; n_min = i;

		for (int j = i; j < n; j++) 
		{
			if (strcmp(a[j].author, min.author) < 0) 
			{
				min = a[j];
				n_min = j;
			}
		}

		a[n_min] = a[i];
		a[i] = min;
	}
}



void input(booker* book, int n) 
/*Ручной ввод данных о n книгах*/
{

	cout << "\nEnter " << n;

	cout << " books with atributes (code, author, title, year, place (the shelf number)) separated by spaces> ";

	cout << endl;

	for (int i = 0; i < n; i++) 
	{

		cin >> book[i].code >> book[i].author >> book[i].title >> book[i].year >> book[i].place;

	}

}



void output(booker* book, int m, bool py_check = false)
/*Форматированный под таблицу вывод*/
{
	cout << "\n\n\n";

	if (py_check){
		cout << setw(45) << "Top " << m << " novels in the United Kingdom" << "\n\n";
	}

	cout << setw(16) << "Code|";
	cout << setw(31) << "Author|";
	cout << setw(51) << "Title|";
	cout << setw(7) << "Year|";
	cout << setw(7) << "Place|";
	cout << endl;


	for (int i = 0; i < m; i++) 
	{
		cout << setw(112) << "________________________________________________________________________________________________" << endl;
		cout << setw(15) << book[i].code << "|";
		cout << setw(30) << book[i].author << "|";
		cout << setw(50) << book[i].title << "|";
		cout << setw(6) << book[i].year << "|";
		cout << setw(6) << book[i].place << "|";
		cout << endl;
	}
}



void books_of_author(booker book[], int n)
/*Нахождение и вывод всех книг авторов до 0
O(n) поиск*/
{
	string author;
	bool running;
	int count_books = 0;

	running = true;
	while (running) 
	{
		cout << "\n\nEnter the desire author ('0' to exit)> ";

		cin >> author;

		if (author != "0") 
		{
			cout << author << "'s books:";

			for (int i = 0; i < n; i++) 
			{
				if (book[i].author == author) 
				{
					cout << "\n" << book[i].code << " " << book[i].title;
					count_books++;
				}
			}

			if (count_books == 0) 
			{
				cout << "None";
			}
		}

		else running = false;

	}
}



void bin_book_search(booker book[], int n)
{
/*Бинарный поиск для левой границы и проход до крайнего правого*/
	char author[30] = "12";
	bool running;

	running = true;
	while (running) 
	{
		int count_books = 0, mid;
		cout << "\n\nEnter the desire author ('0' is exit)> ";

		cin >> author;

		if ((strcmp("0", author) == 0)) 
		{
			running = false;
		}

		else
		{
			cout << author << "'s books: " << endl;

			// Бин поиск
			int left = -1, right = n; 
			while (right - left > 1)
			{
				mid = (right + left) / 2;
			    if (strcmp(book[mid].author, author) < 0) left = mid; 
			    else right = mid;  
			}

			// Выписывание книг подряд
			while (strcmp(book[right].author, author) == 0)
			{
				cout << "\t" << book[right].code << "|\t" << book[right].title << endl;
				++right;
				++count_books;
			}

			// Отсутствие книг атора
			if (count_books == 0)
			{
				cout << "None" << endl;
			}
		}
	}
}




void py()
/*Считывание ТОП n книг и запись их данных в файл.
После считывания - файл удаляется*/
{
	// Зпуск скрипта
	system("python3 bookScript.py");

	int n;
	ifstream file("data.txt");

	file >> n;

	booker* book = new booker[n];

	for (int i = 0; i < n; i++) {
		file >> book[i].code;
		file >> book[i].author;
		file >> book[i].title;
		file >> book[i].year;
		file >> book[i].place;
	}

	sort_by_author(book, n);
	output(book, n, true);
	//books_of_author(book, n);
	bin_book_search(book, n);

	file.close();

	system("rm data.txt");

}

// ОСНОВА 7 ЛАБЫ ----------------------------------------------

int main()
{

	cout << "Would you to enter yourself or 'The Big Read'(1/any key)> ";

	int mod;

	cin >> mod;

	if (mod == 1) 
	{
		int n;

		cout << "\n\nEnter the number of books> ";
		cin >> n;

		booker* book = new booker[n];

		input(book, n);
		sort_by_author(book, n);
		output(book, n);
		//books_of_author(book, n);
		bin_book_search(book, n);
	}

	else 
	{
		py();
	}

	return 0;
}