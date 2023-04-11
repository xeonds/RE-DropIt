using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace RE_DropIt
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            Directory_Load();
        }

        private void Directory_Load()
        {
            var directory = new ObservableCollection<DirectoryRecord>();

            foreach (var drive in DriveInfo.GetDrives())
            {
                directory.Add(
                    new DirectoryRecord
                    {
                        Info = new DirectoryInfo(drive.RootDirectory.FullName)
                    }
                );
            }

            dirTreeView.ItemsSource = directory;
        }

        private void FileInfoColumn_Load(object sender, DataGridAutoGeneratingColumnEventArgs e)
        {
            List<string> requiredProperties = new List<string>
            {
                "Name", "Length", "FullName", "IsReadOnly", "LastWriteTime"
            };

            if (!requiredProperties.Contains(e.PropertyName))
            {
                e.Cancel = true;
            }
            else
            {
                e.Column.Header = e.Column.Header.ToString();
            }
        }

        private void button_folder_dropit_Click(object sender, RoutedEventArgs e)
        {
            Console.WriteLine(fileInfo.SelectedValue);
            var proc = new Core(fileInfo.SelectedValuePath);
            proc.Run();
        }
    }

    public class DirectoryRecord
    {
        public DirectoryInfo Info { get; set; }

        public IEnumerable<FileInfo> Files
        {
            get
            {
                try { 
                    return Info.GetFiles();
                }
                catch (Exception)
                {
                    return null;
                }
            }
        }

        public IEnumerable<DirectoryRecord> Directories
        {
            get
            {
                try
                {
                    return from di in Info.GetDirectories("*", SearchOption.TopDirectoryOnly)
                           select new DirectoryRecord { Info = di };
                }
                catch (Exception)
                {
                    return null;
                }
                
            }
        }
    }
}
