'use client';

import { useState, useEffect } from 'react';
import TeamsTableUser from '@/components/user/teamsTable';
import { Container } from 'react-bootstrap';

interface Team {
    team_id: number;
    name: string;
    description: string;
}

// Datos de ejemplo
const sampleTeams: Team[] = [
    { team_id: 1, name: 'Los Halcones', description: 'Equipo de baloncesto masculino' },
    { team_id: 2, name: 'Las Águilas', description: 'Equipo de voleibol femenino' },
    { team_id: 3, name: 'Tigres', description: 'Equipo de fútbol mixto' },
    { team_id: 4, name: 'Leones', description: 'Equipo de atletismo' },
];

export default function TeamsPage() {
    const [teams, setTeams] = useState<Team[]>(sampleTeams);
    const [search, setSearch] = useState('');

    const filteredTeams = (teams || []).filter(team =>
        team.name.toLowerCase().includes(search.toLowerCase()) ||
        team.description.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <Container>
            <TeamsTableUser teams={filteredTeams} />
        </Container>
    );
}
