using System;

namespace MyProject.Core
{
    /// <summary>
    /// A sample class for testing C# API extraction.
    /// </summary>
    public class SampleService : IDisposable
    {
        private readonly string _id;

        public string Name { get; set; }

        public SampleService(string id)
        {
            _id = id;
        }

        /// <summary>
        /// Performs an operation.
        /// </summary>
        public void DoWork(int count, string message = "default")
        {
            Console.WriteLine($"{_id}: {message} {count} times.");
        }

        protected virtual void Dispose(bool disposing)
        {
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }
    }

    public enum ServiceStatus
    {
        Idle,
        Running,
        Error
    }
}
