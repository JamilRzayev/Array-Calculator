using System;

class Program
{
public static void Max(int[] arr)
    {
        int max = arr[0];
        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] > max)
                max = arr[i];
        }
        Console.WriteLine(max);
    }
    public static void Min(int[] arr)
    {
        int min = arr[0];
        for (int i = 0; i < arr.Length; i++)
        {
            if (min > arr[i])
                min = arr[i];
        }
        Console.WriteLine(min);
    }

    public static void Average(int[] arr)
    {
        int result = 0;
        for (int i = 0; i < arr.Length; i++)
        {
            result += arr[i];
        }
        Console.WriteLine((double)result / (double)arr.Length);
    }
    public static void Sum(int[] arr)
    {
        int result = 0;
        for (int i = 0; i < arr.Length; i++)
        {
            result += arr[i];
        }
        Console.WriteLine(result);
    }
    public static void Sort(int[] arr)
    {
        for (int i = 0; i < arr.Length - 1; i++)
        {
            for (int j = 0; j < arr.Length - i - 1; j++)
            {
                if (arr[j] > arr[j + 1])
                {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        foreach (int i in arr)
            Console.Write(i + " ");

    }
    static void Main()

    {
        int a, x;
        Console.WriteLine("Введите длину массива: ");
        x = int.Parse(Console.ReadLine());
        int[] arr = new int[x];
        for (int i = 0; i < x; i++)
        {
            Console.WriteLine($"Введите {i + 1} число: ");
            arr[i] = int.Parse(Console.ReadLine());
        }
        while (true)
        {
            Console.WriteLine("1.Найти максимум массива\n2.Найти минимум массива\n3.Найти среднее значение массива\n4.Найти сумма массива\n5.Отсортировать массив\n0.Выход");
            a = int.Parse(Console.ReadLine());
            switch (a)
            {
                case 0:
                    return;
                case 1:
                    Max(arr);
                    break;
                case 2:
                    Min(arr);
                    break;
                case 3:
                    Average(arr);
                    break;
                case 4:
                    Sum(arr);
                    break;
                case 5:
                    Sort(arr);
                    break;

            }
        }


    }
}
