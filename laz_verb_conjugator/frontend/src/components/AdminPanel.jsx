import { Link } from "react-router-dom";

const AdminPanel = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="max-w-4xl mx-auto p-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Admin</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <Link
            to="/admin/manage-verbs"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-3">
              Manage verbs
            </h2>
            <p className="text-gray-600">
              Dynamically update verbs’ information.
            </p>
          </Link>
          <Link
            to="/admin/backup-database"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-3">
              Backup database
            </h2>
            <p className="text-gray-600">
              Click to download the up-to-date database.
            </p>
          </Link>
        </div>
      </div>
      <div className="text-center mt-6">
        <p className="text-gray-700 text-sm">
          <Link to="/admin/logout">Sign out</Link>
        </p>
      </div>
    </div>
  );
};

export default AdminPanel;
