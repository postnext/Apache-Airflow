import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import liquibase.Liquibase;
import liquibase.database.Database;
import liquibase.database.jvm.HibernateDatabase;
import liquibase.resource.ClassLoaderResourceAccessor;
import java.util.logging.Logger;

public class MigrationManager {
    private static final Logger logger = Logger.getLogger("MigrationManager");
    private static SessionFactory sessionFactory;

    public static void main(String[] args) {
        try {
            sessionFactory = new Configuration().configure().buildSessionFactory();
            runMigrations();
        } catch (Exception e) {
            logger.severe("Database migration failed: " + e.getMessage());
            throw new RuntimeException("Migration error", e);
        }
    }

    public static void runMigrations() {
        try {
            Database database = new HibernateDatabase();
            database.setConnection(sessionFactory.getSessionFactoryOptions().getServiceRegistry()
                    .getService(org.hibernate.engine.jdbc.connections.spi.ConnectionProvider.class)
                    .getConnection());

            Liquibase liquibase = new Liquibase("db/changelog.xml", new ClassLoaderResourceAccessor(), database);
            liquibase.update("");
            logger.info("Database migrations applied successfully.");
        } catch (Exception e) {
            logger.severe("Migration error: " + e.getMessage());
        }
    }
}
