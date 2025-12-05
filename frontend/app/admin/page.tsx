'use client';

import Link from 'next/link';

export default function AdminDashboard() {
    return (
        <div className="container mt-4">

            {/* Header */}
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1 className="fw-bold">Admin Panel</h1>
                <Link href="/logout" className="btn btn-outline-danger btn-sm">
                    Logout
                </Link>
            </div>

            <div className="row">

                {/* Main Content */}
                <div className="col-md-9">
                    <div className="card shadow-sm mb-4">
                        <div className="card-body">
                            <h2 className="fw-semibold">Welcome to the Admin Dashboard</h2>
                            <p className="text-muted">
                                Use the modules below to manage the system quickly.
                            </p>
                        </div>
                    </div>

                    {/* Quick Action Cards */}
                    <div className="row g-4">

                        <div className="col-md-6">
                            <div className="card shadow-sm h-100">
                                <div className="card-body">
                                    <h4 className="fw-bold">
                                        <i className="fas fa-users text-primary me-2"></i>
                                        Teams
                                    </h4>
                                    <p className="text-muted">
                                        Create, edit and delete teams in the system.
                                    </p>
                                    <Link href="/admin/team" className="btn btn-primary">
                                        Manage Teams
                                    </Link>
                                </div>
                            </div>
                        </div>

                        <div className="col-md-6">
                            <div className="card shadow-sm h-100">
                                <div className="card-body">
                                    <h4 className="fw-bold">
                                        <i className="fas fa-user text-success me-2"></i>
                                        Players
                                    </h4>
                                    <p className="text-muted">
                                        Add players, update info or remove records.
                                    </p>
                                    <Link href="/admin/player" className="btn btn-success">
                                        Manage Players
                                    </Link>
                                </div>
                            </div>
                        </div>

                        {/* Puedes agregar más tarjetas aquí si quieres */}

                    </div>
                </div>
            </div>
        </div>
    );
}
