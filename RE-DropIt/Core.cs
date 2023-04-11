using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Windows.Documents;

namespace RE_DropIt
{
    public class Core
    {
        private string path_workdir;
        private enum ProcRule { DELETE, MOVE, RENAME };
        private Dictionary<string, ProcRule> rules;

        public Core(string SelectedPath)
        {
            path_workdir = SelectedPath;
            InitRules();
            ProcessFiles();
        }
        public Run()
        {
            ProcessFiles(path_workdir);
        }

        private bool InitRules()
        {
            return true;
        }

        private bool ProcessFiles(string dir = "")
        {
            if (dir == "") dir = path_workdir;
            var files = Directory.GetFiles(dir);
            var dirs = Directory.GetDirectories(dir);

            foreach(var file in files)
            {
                var fileName = Path.GetFileName(file);
                foreach(var rule in rules)
                {
                    var exp = new Regex(rule.Key);
                    if (exp.Match(file).Success)
                    {
                        ProcessFile(file, rule.Value);
                        break;
                    }
                }
                // no rules matches, should be listed in console.
            }
            foreach (var _dir in dirs)
            {
                var fileName = Path.GetDirectoryName(_dir);
                foreach (var rule in rules)
                {
                    var exp = new Regex(rule.Key);
                    if (exp.Match(_dir).Success)
                    {
                        ProcessDir(_dir, rule.Value);
                        break;
                    }
                }
                // no rules matches, should be listed in console.
            }
            return true;
        }

        private bool ProcessFile(string file_name, ProcRule rule)
        {
            switch (rule)
            {
                case ProcRule.RENAME:
                    break;
                case ProcRule.MOVE:
                    break;
                case ProcRule.DELETE:
                    break;
                default:
                    break;
            }
            return true;
        }

        private bool ProcessDir(string dir_name, ProcRule rule)
        {
            switch (rule)
            {
                case ProcRule.RENAME:
                    break;
                case ProcRule.MOVE:
                    break;
                case ProcRule.DELETE:
                    break;
                default:
                    break;
            }
            return true;
        }
    }
}
