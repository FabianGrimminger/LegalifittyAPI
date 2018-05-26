package com.example.demo.Repositories;

import com.example.demo.Graffity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface GraffityRepository extends JpaRepository<Graffity, Long> {

    @Query(value = "SELECT * FROM graffiy g WHERE g.uuid = ?1", nativeQuery = true)
    Optional<Graffity> findByUUID(UUID uuid);

}
